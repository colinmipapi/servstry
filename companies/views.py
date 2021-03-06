import json

from django.utils import timezone
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from contact_trace.settings import (
    DEBUG,
    STRIPE_LIVE_PUBLIC_KEY,
    STRIPE_TEST_PUBLIC_KEY,
    STRIPE_LIVE_SECRET_KEY,
    STRIPE_TEST_SECRET_KEY
)

from contact_trace.documents.guest_visit_documents import GuestVisitIndex

from billing.models import (
    Subscription,
    PaymentMethod,
    Invoice
)

from companies.models import (
    Company,
    SAFETY_POLICY_HELP_TEXT
)
from companies.forms import (
    NameAddressForm,
    ContactInfoForm,
    LogoForm,
    CoverImgForm,
    EditCompanyInfoForm,
    BrandSettingsForm
)
from companies.decorators import user_is_company_admin
from track.models import (
    GuestVisit,
    CustomSafetyPolicy
)
from track.forms import (
    GuestVisitForm,
    UserVisitForm,
    GuestVisitFilterForm,
    GuestVisitExportForm,
    CustomSafetyPolicyForm
)
from track.backends import (
    get_client_ip,
)
from users.forms import (
    InviteSingleUserForm,
    EditUserForm,
    CustomPasswordChangeForm
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
        'logo_white': True,
    })


@login_required
def create_contact_info(request):
    if 'company_id' in request.session:
        company = Company.objects.get(public_id=request.session['company_id'])
    else:
        companies = Company.objects.filter(admins=request.user).order_by('-created')
        if companies:
            company = companies[0]
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
        companies = Company.objects.filter(admins=request.user).order_by('-created')
        if companies:
            company = companies[0]
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
        companies = Company.objects.filter(admins=request.user).order_by('-created')
        if companies:
            company = companies[0]
        else:
            return redirect('create_company_name_address')

    if not company.customer_id:
        customer = stripe.Customer.create(
            email=request.user.email,
        )
        company.customer_id = customer.id
        company.save()

    return render(request, 'companies/company/register/create-payment.html', {
        'logo_white': True,
        'company': company,
        'stripe_public_key': stripe_public_key,
        'price_id': price_id,
    })


def company_profile(request, slug):

    company = Company.objects.get(slug=slug)
    company_user = company.is_company_user(request.user)

    if company.status != 'SB' and not company_user:
        raise Http404

    if request.method == 'POST':
        if request.user.is_authenticated:
            guest_visit_form = UserVisitForm(request.POST)
        else:
            guest_visit_form = GuestVisitForm(request.POST)
        if guest_visit_form.is_valid():
            email_2 = guest_visit_form.cleaned_data['email_2']
            if email_2 != '':
                return HttpResponse(status=403)
            gv = guest_visit_form.save(commit=False)
            gv.company = company
            gv.ip_address = get_client_ip(request)
            if request.user.is_authenticated and not company_user:
                gv.add_user_information(request.user)
            else:
                gv.save()
            return redirect('confirmation_page', code=gv.confirmation)
        else:
            print(guest_visit_form.errors)

    if company.safety_policy_setting in ['B', 'CB']:
        safety_initial = True
    else:
        safety_initial = False

    if company_user:
        logo_form = LogoForm(instance=company)
        cover_img_form = CoverImgForm(instance=company)
        edit = True
        company_info_form = EditCompanyInfoForm(instance=company)
        nav = True
        guest_visit_form = GuestVisitForm(initial={
            'arrival': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'safety_policy_accept': safety_initial
        })
    else:
        logo_form = False
        cover_img_form = False
        company_info_form = False
        edit = False
        if request.user.is_authenticated:
            nav = True
            guest_visit_form = UserVisitForm(initial={
                'user': request.user,
                'arrival': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                'safety_policy_accept': safety_initial
            })
        else:
            nav = False
            guest_visit_form = GuestVisitForm(initial={
                'arrival': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                'safety_policy_accept': safety_initial
            })

    return render(request, 'companies/profile.html', {
        'company': company,
        'company_user': company_user,
        'logo_form': logo_form,
        'cover_img_form': cover_img_form,
        'company_info_form': company_info_form,
        'edit': edit,
        'nav': nav,
        'guest_visit_form': guest_visit_form
    })


@login_required
@user_is_company_admin
def settings(request, slug, **kwargs):
    company = Company.objects.get(slug=slug)
    if request.user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(admins=request.user).order_by('-created')

    edit_user_info_form = EditUserForm(instance=request.user)
    company_info_form = EditCompanyInfoForm(instance=company)
    change_password_form = CustomPasswordChangeForm(request.user)
    brand_settings_form = BrandSettingsForm(instance=company)
    invite_admin_form = InviteSingleUserForm()

    try:
        subscription = Subscription.objects.get(
            company=company,
            status__in=['active', 'past_due', 'unpaid', 'trailing']
        )
    except:
        subscription = None
    if company.default_payment_method:
        payment_methods = PaymentMethod.objects.filter(
            company=company
        ).exclude(id=company.default_payment_method.id)
    else:
        payment_methods = None
    invoices = Invoice.objects.filter(
        company=company,
        status__in=['open', 'paid']
    )

    google = False
    facebook = False

    for account in request.user.socialaccount_set.all().iterator():

        if account.provider == "google":
            google = account.id
        elif account.provider == "facebook":
            facebook = account.id

    if 'tab' in kwargs:
        tab = kwargs['tab']
    else:
        tab = 'personal'

    safety_policy = CustomSafetyPolicy.objects.filter(company=company).exists()
    if safety_policy:
        custom_safety_policy_form = CustomSafetyPolicyForm(instance=company.safety_policy)
    else:
        custom_safety_policy_form = CustomSafetyPolicyForm()

    return render(request, 'companies/settings.html', {
        'companies': companies,
        'company': company,
        'company_info_form': company_info_form,
        'edit_user_info_form': edit_user_info_form,
        'change_password_form': change_password_form,
        'brand_settings_form': brand_settings_form,
        'invite_admin_form': invite_admin_form,
        'google': google,
        'facebook': facebook,
        'subscription': subscription,
        'payment_methods': payment_methods,
        'invoices': invoices,
        'stripe_public_key': stripe_public_key,
        'safety_policy_help_json': json.dumps(SAFETY_POLICY_HELP_TEXT),
        'custom_safety_policy_form': custom_safety_policy_form,
        'company_admin': True,
        'tab': tab,
        'fixed_nav': True,
    })


@login_required
@user_is_company_admin
def new_subscription(request, slug):

    company = Company.objects.get(slug=slug)
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


@login_required
@user_is_company_admin
def company_dashboard_guest_card_search(request, slug):
    company = Company.objects.get(slug=slug)
    if request.user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(admins=request.user).order_by('-created')
    q = request.POST.get('search')

    s = GuestVisitIndex.search().filter("match", company__id=company.id)
    guests = s.filter("match", confirmation=q).to_queryset()
    if not guests:
        id_list = []
        guests = s.suggest('name_suggestions', q, completion={'field': 'name.suggest'})
        suggestions = guests.execute()
        suggestions = suggestions.suggest.name_suggestions[0]['options']
        for suggestion in suggestions:
            id_list.append(suggestion['_id'])
        guests = GuestVisit.objects.filter(id__in=id_list)

    guest_filter_form = GuestVisitFilterForm()
    export_contacts_form = GuestVisitExportForm()

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
        'search_value': q,
        'fixed_nav': True,
    })


@login_required
@user_is_company_admin
def company_dashboard(request, slug):
    request.session['company_id'] = None

    company = Company.objects.get(slug=slug)
    if request.user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(admins=request.user).order_by('-created')
    filter_contacts_initial = {}
    export_contacts_initial = {}

    if request.method == 'POST':
        guest_filter_form = GuestVisitFilterForm(request.POST)
        if guest_filter_form.is_valid():
            start = guest_filter_form.cleaned_data['start_filter']
            end = guest_filter_form.cleaned_data['end_filter']
            if start and end:
                guests = GuestVisit.objects.filter(
                    company=company,
                    arrival__range=(start, end)
                ).order_by('-arrival')
                filter_contacts_initial['start_filter'] = start
                filter_contacts_initial['end_filter'] = end
                export_contacts_initial['start_export'] = start
                export_contacts_initial['end_export'] = end
            elif start:
                guests = GuestVisit.objects.filter(
                    company=company,
                    arrival__gte=start
                ).order_by('-arrival')
                filter_contacts_initial['start_filter'] = start
                export_contacts_initial['start_export'] = start
            elif end:
                guests = GuestVisit.objects.filter(
                    company=company,
                    arrival__lte=end
                ).order_by('-arrival')
                filter_contacts_initial['end_filter'] = end
                export_contacts_initial['end_export'] = end
            else:
                guests = GuestVisit.objects.filter(
                    company=company,
                ).order_by('-arrival')
        else:
            guests = GuestVisit.objects.none()
            print(guest_filter_form.errors)
    else:
        guests = GuestVisit.objects.filter(company=company).order_by('-arrival')

    guest_filter_form = GuestVisitFilterForm(
        initial=filter_contacts_initial
    )
    export_contacts_form = GuestVisitExportForm(
        initial=export_contacts_initial
    )

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
    if request.user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(admins=request.user).order_by('-created')
    if companies:
        return redirect('company_dashboard', slug=companies[0].slug)
    elif not request.user.first_name or not request.user.last_name or not request.user.email:
        return redirect('user-contact-info')
    else:
        return redirect('create_company_name_address')


def custom_safety_policy(request, slug):
    try:
        company = Company.objects.get(slug=slug)
        safety_policy = company.safety_policy
    except:
        raise Http404

    company_user = company.is_company_user(request.user)
    custom_safety_policy_form = CustomSafetyPolicyForm(instance=safety_policy)

    return render(request, 'track/custom_safety_policy.html', {
        'company': company,
        'safety_policy': safety_policy,
        'company_user': company_user,
        'custom_safety_policy_form': custom_safety_policy_form
    })


class CompanyAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Company.objects.all().order_by('-created')[:5]

        if self.q:
            qs = qs.filter(name__istartswith=self.q)[:5]

        return qs