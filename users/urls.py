from django.urls import path

from users import views

urlpatterns = [
    path(
        'user-settings/',
        views.user_settings,
        name='user_settings'
    ),
    path(
        '',
        views.user_home,
        name='user_home'
    )
]
