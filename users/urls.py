from django.urls import path

from users import views

urlpatterns = [
    path(
        'settings/<str:tab>/',
        views.user_settings,
        name='user_settings_tab'
    ),
    path(
        'settings/',
        views.user_settings,
        name='user_settings'
    ),
    path(
        '<str:tab>/',
        views.user_home,
        name='user_home_tab'
    ),
    path(
        '',
        views.user_home,
        name='user_home'
    )
]
