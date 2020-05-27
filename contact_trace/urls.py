from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from users.views import (
    landing,
    business_landing,
    home,
    contact_us
)

urlpatterns = [
    path(
        'api/',
        include('contact_trace.api_urls')
    ),
    path(
        'profile/',
        include('users.urls')
    ),
    path(
        'register/',
        include('contact_trace.signup_urls')
    ),
    path(
        'cm/',
        include('companies.profile_urls')
    ),
    path(
        'dashboard/',
        include('companies.dashboard_urls')
    ),
    path(
        'confirm/',
        include('track.urls')
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    # Django Allauth Library (https://github.com/pennersr/django-allauth)
    path(
        'accounts/',
        include('allauth.urls')
    ),
    path(
        'help/',
        TemplateView.as_view(template_name='help.html'),
        name='help'
    ),
    path(
        'privacy-policy/',
        TemplateView.as_view(template_name='privacy_policy.html'),
        name='privacy_policy'
    ),
    path(
        'terms-and-conditions/',
        TemplateView.as_view(template_name='terms_and_conditions.html'),
        name='terms_and_conditions'
    ),
    path(
        'contact-us/',
        contact_us,
        name='contact_us'
    ),
    path(
        'landing/',
        landing,
        name='landing'
    ),
    path(
        'business/',
        business_landing,
        name='business_landing'
    ),
    path(
        '',
        home,
        name='home'

    )
]

handler400 = 'users.views.handler400'
handler403 = 'users.views.handler403'
handler404 = 'users.views.handler404'
handler500 = 'users.views.handler500'
