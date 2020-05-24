from django.http import Http404
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from contact_trace.documents.company_document import CompanyIndex

from companies.models import Company
from companies.forms import (
    LogoForm,
    CoverImgForm,
    EditCompanyInfoForm,
)

from companies.serializer import (
    CompanySerializer
)

from users.forms import (
    InviteSingleUserForm,
)


class CompanySuggestView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        results_list = []
        name = request.POST.get('search')

        s = CompanyIndex.search().query('match', name=name)[:5]
        print(s.to_queryset())
        for item in s:
            item_dict = {
                'name': item.name,
                'link': item.get_absolute_url
            }
            results_list.append(item_dict)

        return JsonResponse(results_list, safe=False)


@api_view(['POST', ])
def profile_img(request, public_id):
    try:
        company = Company.objects.get(public_id=public_id)
    except:
        raise Http404
    if company.is_company_user(request.user):
        form = LogoForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company_result = form.save()
            data = {
                'imgUrl': company_result.logo_url,
                'backgroundColor': company_result.logo_background_color
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def cover_img(request, public_id):
    try:
        company = Company.objects.get(public_id=public_id)
    except:
        raise Http404
    if company.is_company_user(request.user):
        form = CoverImgForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company_result = form.save()
            data = {
                'imgUrl': company_result.get_cover_img_url,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def invite_page_admin(request, public_id):
    try:
        company = Company.objects.get(public_id=public_id)
    except:
        raise Http404
    if company.is_company_user(request.user):
        form = InviteSingleUserForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            company.admins.add(user)
            company.save()
            data = {
                'result': 'success',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def company_info_form(request, public_id):
    try:
        company = Company.objects.get(public_id=public_id)
    except:
        raise Http404

    if company.is_company_user(request.user):
        company
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

    form = EditCompanyInfoForm(request.POST, instance=company)
    if form.is_valid():
        result = form.save()
        serializer = CompanySerializer(result)
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

