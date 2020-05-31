from django.utils import timezone
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm

from contact_trace.settings import (
    DEBUG,
    STRIPE_LIVE_PUBLIC_KEY,
    STRIPE_TEST_PUBLIC_KEY,
    STRIPE_LIVE_SECRET_KEY,
    STRIPE_TEST_SECRET_KEY
)

from companies.models import Company
from companies.forms import (
    NameAddressForm,
    ContactInfoForm,
    LogoForm,
    CoverImgForm,
    EditCompanyInfoForm,
)
from track.models import (
    GuestVisit,
)
from track.forms import (
    GuestVisitForm,
    GuestVisitFilterForm,
    GuestVisitExportForm
)
from track.backends import (
    get_client_ip,
)
from track.tasks import (
    send_confirmation_code_email,
)
from users.forms import (
    InviteSingleUserForm,
    EditUserForm,
)

from dal import autocomplete
import stripe

if DEBUG:
    stripe_public_key = STRIPE_TEST_PUBLIC_KEY
    stripe.api_key = STRIPE_TEST_SECRET_KEY
    price_id = "plan_HLXj0nHWUjJdbR"
else:
    stripe_public_key = STRIPE_LIVE_PUBLIC_KEY
    stripe.api_key = STRIPE_LIVE_SECRET_KEY
    price_id = 'plan_HKrTzC63N6wns9'


@login_required
def create_company_name_address(request):
    if request.method == 'POST':
        form = NameAddressForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.status = 'SB'
            company.save()
            company.admins.add(request.user)
            form.save_m2m()
            company.update_gmaps_data()
            request.session['company_id'] = str(company.public_id)
            return redirect('create_contact_info')
    else:
        try:
            company = Company.objects.get(public_id=request.session['company_id'])
            form = NameAddressForm(instance=company)
        except:
            form = NameAddressForm()
    return render(request, 'companies/company/register/create-name-address.html', {
        'form': form,
    })


@login_required
def create_contact_info(request):
    if 'company_id' in request.session:
        company = Company.objects.get(public_id=request.session['company_id'])
    else:
        return redirect('create_company_name_address')
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('create_invite_admins')
    else:
        form = ContactInfoForm(instance=company)
    return render(request, 'companies/company/register/create-contact-info.html', {
        'logo_blue': True,
        'form': form,
    })


@login_required
def create_invite_admins(request):
    if 'company_id' in request.session:
        company = Company.objects.get(public_id=request.session['company_id'])
    else:
        return redirect('create_company_name_address')

    if request.method == 'POST':
        form = InviteSingleUserForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['company_id'] = None
            return redirect('home')
    else:
        form = InviteSingleUserForm()

    return render(request, 'companies/company/register/create-invite-admins.html', {
        'logo_blue': True,
        'company': company,
        'form': form
    })


@login_required
def create_payment(request):
    if 'company_id' in request.session:
        company = Company.objects.get(public_id=request.session['company_id'])
    else:
        return redirect('create_company_name_address')

    if not company.customer_id:
        customer = stripe.Customer.create(
            email=request.user.email,
        )
        company.customer_id = customer.id
        company.save()

    return render(request, 'companies/company/register/create-payment.html', {
        'logo_blue': True,
        'company': company,
        'stripe_public_key': stripe_public_key,
        'price_id': price_id,
    })


def company_profile(request, slug):

    company = Company.objects.get(slug=slug)

    if company.status != 'SB':
        raise Http404

    if request.method == 'POST':
        guest_visit_form = GuestVisitForm(request.POST)
        if guest_visit_form.is_valid():
            gv = guest_visit_form.save(commit=False)
            gv.company = company
            gv.ip_address = get_client_ip(request)
            gv.save()
            send_confirmation_code_email.apply_async([gv.id, ])
            return redirect('confirmation_page', code=gv.confirmation)

    company_user = company.is_company_user(request.user)

    if company_user:
        logo_form = LogoForm(instance=company)
        cover_img_form = CoverImgForm(instance=company)
        edit = True
        company_info_form = EditCompanyInfoForm(instance=company)
    else:
        logo_form = False
        cover_img_form = False
        company_info_form = False
        edit = False

    if request.user.is_authenticated:
        nav = True
    else:
        nav = False

    guest_visit_form = GuestVisitForm(initial={
        'arrival': timezone.now().strftime('%Y-%m-%dT%H:%M'),
    })

    return render(request, 'companies/profile.html', {
        'company': company,
        'company_user': company_user,
        'logo_form': logo_form,
        'cover_img_form': cover_img_form,
        'company_info_form': company_info_form,
        'edit': edit,
        'nav': nav,
        'guest_visit_form': guest_visit_form,
    })


@login_required
def settings(request, slug):
    company = Company.objects.get(slug=slug)
    companies = Company.objects.filter(admins=request.user).order_by('-created')

    edit_user_info_form = EditUserForm(instance=request.user)
    company_info_form = EditCompanyInfoForm(instance=company)
    change_password_form = PasswordChangeForm(request.user)
    invite_admin_form = InviteSingleUserForm()

    google = False
    facebook = False

    for account in request.user.socialaccount_set.all().iterator():

        if account.provider == "google":
            google = account.id
        elif account.provider == "facebook":
            facebook = account.id

    return render(request, 'companies/settings.html', {
        'companies': companies,
        'company': company,
        'company_info_form': company_info_form,
        'edit_user_info_form': edit_user_info_form,
        'change_password_form': change_password_form,
        'invite_admin_form': invite_admin_form,
        'google': google,
        'facebook': facebook,
        'company_admin': True,
        'tab': 'personal',
        'fixed_nav': True,
    })


@login_required
def company_dashboard(request, slug):
    request.session['company_id'] = None

    company = Company.objects.get(slug=slug)
    companies = Company.objects.filter(admins=request.user).order_by('-created')
    export_contacts_inital = {}

    if request.method == 'POST':
        guest_filter_form = GuestVisitFilterForm(request.POST)
        if guest_filter_form.is_valid():
            start = guest_filter_form.cleaned_data['start']
            end = guest_filter_form.cleaned_data['end']
            guests = GuestVisit.objects.filter(
                company=company,
            ).order_by('-arrival')
            if start:
                guests.filter(arrival__gte=start)
                export_contacts_inital['start'] = start
            if end:
                guests.filter(arrival__lte=end)
                export_contacts_inital['end'] = end
        else:
            guests = GuestVisit.objects.none()
            print(guest_filter_form.errors)
    else:
        guest_filter_form = GuestVisitFilterForm()
        guests = GuestVisit.objects.filter(company=company).order_by('-arrival')

    export_contacts_form = GuestVisitExportForm(initial=export_contacts_inital)

    paginator = Paginator(guests, 25)

    page = request.GET.get('page')
    guests_page = paginator.get_page(page)

    return render(request, 'companies/dashboard.html', {
        'companies': companies,
        'company': company,
        'company_admin': True,
        'guests_page': guests_page,
        'guest_filter_form': guest_filter_form,
        'export_contacts_form': export_contacts_form,
        'fixed_nav': True,
    })


@login_required
def dashboard(request):

    companies = Company.objects.filter(admins=request.user).order_by('-created')
    if companies:
        return redirect('company_dashboard', slug=companies[0].slug)
    elif not request.user.first_name or not request.user.last_name or not request.user.email:
        return redirect('user-contact-info')
    else:
        return redirect('account_logout')


class CompanyAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Company.objects.all().order_by('-created')[:5]

        if self.q:
            qs = qs.filter(name__istartswith=self.q)[:5]

        return qs