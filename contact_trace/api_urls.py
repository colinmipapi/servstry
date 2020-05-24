from django.urls import path, include

urlpatterns = [
    path(
        'company/',
        include('companies.api_urls')
    ),
    path(
        'track/',
        include('track.api_urls')
    ),
    path(
        'users/',
        include('users.api_urls')
    )
]
