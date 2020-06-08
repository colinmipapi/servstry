from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import mail_admins
from django.core.paginator import Paginator

from track.models import (
    GuestVisit,
)
from users.models import (
    Invitation,
)
from users.forms import (
    UserContactInfoForm,
    RequestDemoForm,
    InvitationSignupForm,
    ContactUsForm,
    EditUserForm,
    CustomPasswordChangeForm,
    NotificationSettings,
    CustomSocialSignupForm
)

from allauth.account.models import EmailAddress


@login_required
def user_contact_info(request):

    if request.method == 'POST':
        form = UserContactInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if form.cleaned_data['create_business'] is True:
                return redirect('create_company_name_address')
            else:
                return redirect('home')
    else:
        form = UserContactInfoForm(instance=request.user)

    return render(request, 'register/user_contact_info.html', {
        'form': form,
    })


@login_required
def social_user_signup(request):

    if request.method == 'POST':
        form = CustomSocialSignupForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if form.cleaned_data['create_business'] is True:
                return redirect('create_company_name_address')
            else:
                return redirect('home')
    else:
        form = CustomSocialSignupForm(instance=request.user)

    return render(request, 'allauth/social/signup.html', {
        'form': form,
    })


@login_required
def user_settings(request, **kwargs):

    # Contact Info Tab
    edit_user_info_form = EditUserForm(instance=request.user)

    # Password Tab
    change_password_form = CustomPasswordChangeForm(request.user)

    # Notifications Tab
    notification_form = NotificationSettings(instance=request.user)

    # Social Tab
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
        tab = 'contact-info'

    return render(request, 'users/settings.html', {
        'edit_user_info_form': edit_user_info_form,
        'change_password_form': change_password_form,
        'notification_form': notification_form,
        'google': google,
        'facebook': facebook,
        'tab': tab,
        'fixed_nav': True,
    })


@login_required
def user_home(request, **kwargs):

    visits = GuestVisit.objects.filter(user=request.user).order_by('-arrival')

    if 'tab' in kwargs:
        tab = kwargs['tab']
    else:
        tab = 'visits'

    paginator = Paginator(visits, 25)

    page = request.GET.get('page')
    guests_page = paginator.get_page(page)

    return render(request, 'users/home.html', {
        'guests_page': guests_page,
        'tab': tab,
        'fixed_nav': True,
    })


def invitation_signup(request, invitation_id):
    page_title = "Contact Information"
    invitation = Invitation.objects.get(public_id=invitation_id)
    if invitation.accepted:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = InvitationSignupForm(request.POST, instance=invitation.user)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password1'])
                new_user.save()
                try:
                    EmailAddress.objects.create(
                        user=new_user,
                        email=new_user.email,
                        verified=True,
                        primary=True
                    )
                except:
                    print('email already exists error')
                invitation.accepted = True
                invitation.save()
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard')
            else:
                print(form.errors)
        else:
            form = InvitationSignupForm(instance=invitation.user)
            login(request, invitation.user, backend='django.contrib.auth.backends.ModelBackend')

        return render(request, 'register/invite_signup.html', {
            'invitation': invitation,
            'form': form,
            'page_title': page_title,
            'user': request.user,
            'back': False,
            'overflow_y': True,
        })


def landing(request):

    return render(request, 'landing.html', {
        'landing': True,
    })


def business_landing(request):
    demo_form = RequestDemoForm()
    return render(request, 'business_landing.html', {
        'demo_form': demo_form,
        'nav': False,
    })


def home(request):

    if request.user.is_authenticated:
        if request.user.is_company_user:
            return redirect('dashboard')
        else:
            return redirect('user_home')
    else:
        return render(request, 'landing.html', {
            'landing': True,
        })


'''
Error Page Views - industry/urls.py
'''


def handler400(request, exception, template_name="errors/400.html"):
    response = render(
        None,
        template_name,
        context={
            'request': request,
        }
    )
    response.status_code = 400
    return response


def handler403(request, exception, template_name="errors/403.html"):
    response = render(
        None,
        template_name,
        context={
            'request': request,
        }
    )
    response.status_code = 403
    return response


def handler404(request, exception, template_name="errors/404.html"):
    response = render(
        None,
        template_name,
        context={
            'request': request,
        }
    )
    response.status_code = 404
    return response


def handler500(request):
    response = render(
        None,
        "errors/500.html",
        context={
            'request': request,
        }
    )
    response.status_code = 500
    return response


'''
Info Pages
'''


def contact_us(request):
    form_message = None

    if request.method == 'POST':

        contact_us_form = ContactUsForm(request.POST)

        if contact_us_form.is_valid():
            email_2 = contact_us_form.cleaned_data['email_2']
            if email_2 != '':
                return HttpResponse(status=403)
            full_name = contact_us_form.cleaned_data['full_name']
            email = contact_us_form.cleaned_data['email_address']
            user_message = contact_us_form.cleaned_data['message']
            subject = "New Contact Us Form Submission - %s" % (full_name)
            email_text = "New Contact Us Form Submission \r\n Name: %s \r\n Email: %s \r\n Message: %s" % (
            full_name, email, user_message)
            email_html = '<h2 style="color:#597DC6"><b>New Contact Us Form Submission</b></h2><p><b>Name:</b> %s</p><p><b>Email:</b> %s</p><p><b>Message:</b>\r\n%s</p>' % (
            full_name, email, user_message)
            mail_admins(
                subject,
                email_text,
                'Admin Notifications <admin-notifications@servstry.com>',
                html_message=email_html
            )
            contact_us_form = ContactUsForm()
            form_message = "Message Sent! We'll try to get back to you in the next 48 hours."
        else:
            print(contact_us_form.errors)
            return HttpResponse(status=403)

    else:

        if request.user.is_authenticated:

            contact_us_form = ContactUsForm(initial={
                'full_name': request.user.get_full_name,
                'email_address': request.user.email,
            })
        else:
            contact_us_form = ContactUsForm()

    return render(request, 'info-pages/contact_us.html', {
        'contact_us_form': contact_us_form,
        'form_message': form_message,
        'overflow_y': True,
    })