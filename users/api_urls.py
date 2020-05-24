from django.urls import path

from users import api_views as views

urlpatterns = [
    path(
        'demo-request/',
        views.demo_request,
        name='demo_request_api'
    ),
]
