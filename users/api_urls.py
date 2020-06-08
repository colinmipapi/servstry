from django.urls import path

from users import api_views as views

urlpatterns = [
    path(
        'demo-request/',
        views.demo_request,
        name='demo_request_api'
    ),
    path(
        'edit-user-info-form/<uuid:public_id>/',
        views.edit_user_info_form,
        name='edit_user_info_form_api'
    ),
    path(
        'change-password-form/<uuid:public_id>/',
        views.change_password_form,
        name='change_password_form_api'
    ),
    path(
        'notification-settings/<uuid:public_id>/',
        views.notification_form,
        name='notification_form_api'
    )
]
