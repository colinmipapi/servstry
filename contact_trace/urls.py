from django.contrib import admin
from django.urls import path, include

from users.views import landing, business_landing, home

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
