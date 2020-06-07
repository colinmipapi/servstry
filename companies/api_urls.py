from django.urls import path, include

from companies import api_views as views

urlpatterns = [
    path(
        'company-suggest/',
        views.CompanySuggestView.as_view(),
        name='company-suggest'
    ),
    path(
        'profile-img/<uuid:public_id>/',
        views.profile_img,
        name="company_logo_api"
    ),
    path(
        'cover-img/<uuid:public_id>/',
        views.cover_img,
        name="company_cover_img_api"
    ),
    path(
        'invite-page-admin/<uuid:public_id>/',
        views.invite_page_admin,
        name="invite_company_admin_form_api"
    ),
    path(
        'company-info-form/<uuid:public_id>/',
        views.company_info_form,
        name="company_info_form_api"
    ),
    path(
        'brand-settings-form/<uuid:public_id>/',
        views.brand_settings_form,
        name="brand_settings_form_api"
    ),
    path(
        'export-contacts/<uuid:public_id>/',
        views.export_contacts,
        name='export_contacts_api'
    ),
    path(
        'remove-admin/<uuid:company_id>/<uuid:user_id>/',
        views.remove_admin,
        name='remove_admin_api'
    ),
    path(
        'generate-company-flyer/<uuid:company_id>/',
        views.generate_info_flyer,
        name='generate_company_flyer_api'
    ),
    path(
        'download-company-flyer/<uuid:company_id>/',
        views.download_flyer,
        name='download_company_flyer_api'
    )
]
