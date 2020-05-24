from django.urls import path

from companies import views

urlpatterns = [
    path(
        'company-autocomplete/',
        views.CompanyAutocomplete.as_view(),
        name='company-autocomplete'
    ),
    path(
        '<str:slug>/',
        views.company_profile,
        name="company_profile"
    ),
]
