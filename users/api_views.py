from users.backends import demo_request_email
from users.forms import RequestDemoForm

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status


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