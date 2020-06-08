from django.http import Http404
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

from users.backends import demo_request_email
from users.models import (
    CustomUser,
)
from users.forms import (
    EditUserForm,
    RequestDemoForm,
    CustomPasswordChangeForm,
    NotificationSettings
)
from users.serializers import (
    CustomUserSerializer,
)

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.models import SocialAccount


@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
def demo_request(request):
    form = RequestDemoForm(request.POST)
    if form.is_valid():
        data = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'phone': form.cleaned_data['phone'],
            'company': form.cleaned_data['company']
        }
        demo_request_email(data)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def edit_user_info_form(request, public_id):
    try:
        user = CustomUser.objects.get(public_id=public_id)
    except:
        raise Http404

    if request.user == user:
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            result = form.save()
            serializer = CustomUserSerializer(result)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def change_password_form(request, public_id):
    try:
        user = CustomUser.objects.get(public_id=public_id)
    except:
        raise Http404

    if request.user == user:
        form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return Response(status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def notification_form(request, public_id):
    try:
        user = CustomUser.objects.get(public_id=public_id)
    except:
        raise Http404
    if request.user == user:
        form = NotificationSettings(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return Response({}, status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT', ])
def disconnect_social_account(request, account_id, setting_page):
    try:
        account = SocialAccount.objects.get(id=account_id)
    except:
        raise Http404

    if setting_page == 'company':
        setting_redirect = '/dashboard/settings/personal/'
    else:
        setting_redirect = '/profile/settings/social/'

    social_company = account.provider
    connect_url = reverse('provider_login_url', args=[social_company, 'connect', setting_redirect])
    if account.user == request.user:
        account.delete()
        return Response({'url', connect_url}, status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
