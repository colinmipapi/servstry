from django.urls import path

from billing import api_views as views

urlpatterns = [
    path(
        'create-subscription/',
        views.create_subscription,
        name='create-subscription'
    ),
]
