from django.urls import path, include

urlpatterns = [
    path(
        'billing/',
        include('billing.api_urls')
    ),
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
