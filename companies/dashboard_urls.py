from django.urls import path

from companies import views

urlpatterns = [
    path(
        '<str:slug>/settings/',
        views.settings,
        name='company_settings'
    ),
    path(
        '<str:slug>/',
        views.company_dashboard,
        name="company_dashboard"
    ),
    path(
        '',
        views.dashboard,
        name="dashboard"
    ),
]