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
    )
]
