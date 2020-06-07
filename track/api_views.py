from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from companies.models import (
    Company,
)
from track.models import (
    CustomSafetyPolicy,
)
from track.forms import (
    CustomSafetyPolicyForm,
)


@api_view(['POST', ])
def custom_safety_policy_form(request, company_id, **kwargs):

    try:
        company = Company.objects.get(public_id=company_id)
    except:
        raise Http404

    if company.is_company_user(request.user):
        safety_policy = CustomSafetyPolicy.objects.filter(company=company).exists()
        if safety_policy:
            form = CustomSafetyPolicyForm(request.POST, instance=company.safety_policy)
        else:
            form = CustomSafetyPolicyForm(request.POST)
        if form.is_valid():
            custom_safety_policy = form.save(commit=False)
            custom_safety_policy.company = company
            custom_safety_policy.save()
            if 'html' in kwargs:
                data = custom_safety_policy.policy_text
            else:
                data = {}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
