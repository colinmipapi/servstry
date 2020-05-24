from django.urls import path, include

urlpatterns = [
    path(
        'company/',
        include('companies.api_urls')
    ),
]
