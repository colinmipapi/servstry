from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from companies.models import Company
from companies.forms import (
    NameAddressForm,
    ContactInfoForm,
    LogoForm,
    CoverImgForm,
    EditCompanyInfoForm
)
from users.forms import (
    InviteSingleUserForm,
)

from dal import autocomplete


@login_required
def create_company_name_address(request):
    if request.method == 'POST':
        form = NameAddressForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.admin.add(request.user)
            company.save()
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

    if request.method == 'POST':
        form = None
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = None

    return render(request, 'companies/company/register/create-payment.html', {
        'logo_blue': True,
        'form': form,
        'company': company
    })


def company_profile(request, slug):

    company = Company.objects.get(slug=slug)
    company_user = company.is_company_user(request.user)

    if company_user:
        logo_form = LogoForm(instance=company)
        cover_img_form = CoverImgForm(instance=company)
        edit = True
        company_info_form = EditCompanyInfoForm(instance=company)
        nav = True
    else:
        logo_form = False
        cover_img_form = False
        company_info_form = False
        edit = False
        nav = False

    return render(request, 'companies/profile.html', {
        'company': company,
        'company_user': company_user,
        'logo_form': logo_form,
        'cover_img_form': cover_img_form,
        'company_info_form': company_info_form,
        'edit': edit,
        'nav': nav
    })


@login_required
def settings(request, slug):
    company = Company.objects.get(slug=slug)
    companies = Company.objects.filter(admins=request.user).order_by('-created')

    return render(request, 'companies/settings.html', {
        'companies': companies,
        'company': company,
        'company_admin': True,
    })


@login_required
def company_dashboard(request, slug):
    company = Company.objects.get(slug=slug)
    companies = Company.objects.filter(admins=request.user).order_by('-created')

    return render(request, 'companies/dashboard.html', {
        'companies': companies,
        'company': company,
        'company_admin': True,
    })


@login_required
def dashboard(request):

    companies = Company.objects.filter(admins=request.user).order_by('-created')
    if companies:
        company = companies[0]
    else:
        return redirect('account_logout')

    return render(request, 'companies/dashboard.html', {
        'companies': companies,
        'company': company,
        'company_admin': True,
    })


class CompanyAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Company.objects.all().order_by('-created')[:5]

        if self.q:
            qs = qs.filter(name__istartswith=self.q)[:5]

        return qs