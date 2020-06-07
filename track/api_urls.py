from django.urls import path

from track import api_views as views

urlpatterns = [
    path(
        'custom-safety-policy-form/<uuid:company_id>/<str:html>/',
        views.custom_safety_policy_form,
        name='custom_safety_policy_form_html_api'
    ),
    path(
        'custom-safety-policy-form/<uuid:company_id>/',
        views.custom_safety_policy_form,
        name='custom_safety_policy_form_api'
    ),
]
