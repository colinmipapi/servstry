from django.urls import path

from companies.views import (
    create_company_name_address,
    create_contact_info,
    create_invite_admins,
    create_payment,
)
from users.views import user_contact_info

urlpatterns = [
    path(
        'profile-info/',
        user_contact_info,
        name="user-contact-info"
    ),
    path(
        'name-address/',
        create_company_name_address,
        name='create_company_name_address'
    ),
    path(
        'contact-info/',
        create_contact_info,
        name='create_contact_info'
    ),
    path(
        'invite-team/',
        create_invite_admins,
        name='create_invite_admins'
    ),
    path(
        'payment/',
        create_payment,
        name='create_payment'
    ),
]
