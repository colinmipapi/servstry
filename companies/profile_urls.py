from django.urls import path

from companies import views

urlpatterns = [
    path(
        'company-autocomplete/',
        views.CompanyAutocomplete.as_view(),
        name='company-autocomplete'
    ),
    path(
        '<str:slug>/safety-policy/',
        views.custom_safety_policy,
        name='custom_safety_policy'
    ),
    path(
        '<str:slug>/',
        views.company_profile,
        name="company_profile"
    ),
]
