from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from companies.forms import WaitListForm
from users.forms import (
    UserContactInfoForm,
    RequestDemoForm,
)


@login_required
def user_contact_info(request):

    if request.method == 'POST':
        form = UserContactInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('create_company_name_address')
    else:
        form = UserContactInfoForm(instance=request.user)

    return render(request, 'register/user_contact_info.html', {
        'form': form,
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
        return redirect('dashboard')
    else:
        submit = False
        if request.method == 'POST':
            form = WaitListForm(request.POST)
            if form.is_valid():
                form.save()
                submit = True
        else:
            form = WaitListForm()

        return render(request, 'wait_list_landing.html', {
            'form': form,
            'submit': submit,
            'nav': False,
        })
