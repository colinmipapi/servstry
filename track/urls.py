from django.urls import path

from track import views

urlpatterns = [
    path(
        '<str:code>/',
        views.confirmation_page,
        name='confirmation_page'
    ),
]
