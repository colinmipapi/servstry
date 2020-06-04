from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.contenttypes.models import ContentType

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from contact_trace.documents.company_document import CompanyIndex
from contact_trace.utils import generate_unique_username

from companies.models import Company
from companies.forms import (
    LogoForm,
    CoverImgForm,
    EditCompanyInfoForm,
)
from companies.backends import (
    generate_info_flyer_pdf,
)

from companies.serializer import (
    CompanySerializer
)
from track.forms import (
    GuestVisitExportForm,
)
from track.tasks import (
    send_report_email,
)
from users.models import (
    CustomUser,
    Invitation
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
            existing_user = CustomUser.objects.filter(email=form.cleaned_data['email'])
            if existing_user:
                user = existing_user[0]
            else:
                user = CustomUser.objects.create_user(
                    username=generate_unique_username(form.cleaned_data['first_name'], form.cleaned_data['last_name']),
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                Invitation.objects.create(
                    email=form.cleaned_data['email'],
                    user=user,
                    invitation_type='C',
                    inviter_content_type=ContentType.objects.get_for_model(company),
                    inviter_object_id=company.id
                )
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
        form = EditCompanyInfoForm(request.POST, instance=company)
        if form.is_valid():
            result = form.save()
            if not result.place_id and result.address1:
                result.update_gmaps_data()
            serializer = CompanySerializer(result)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def export_contacts(request, public_id):
    try:
        company = Company.objects.get(public_id=public_id)
    except:
        raise Http404

    if company.is_company_user(request.user):
        form = GuestVisitExportForm(request.POST)
        if form.is_valid():
            send_report_email.apply_async([
                company.id,
                request.user.id,
                form.cleaned_data['file_type'],
                form.cleaned_data['start_export'],
                form.cleaned_data['end_export']
            ])
            return Response({'result': 'success', }, status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def remove_admin(request, company_id, user_id):

    try:
        company = Company.objects.get(public_id=company_id)
    except:
        raise Http404

    if company.is_company_user(request.user):
        try:
            admin_user = CustomUser.objects.get(public_id=user_id)
        except:
            raise Http404
        company.admins.remove(admin_user)
        return Response({'result': 'success', }, status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def generate_info_flyer(request, company_id):

    try:
        company = Company.objects.get(public_id=company_id)
    except:
        raise Http404

    if company.is_company_user(request.user):
        data = generate_info_flyer_pdf(company)

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', ])
def download_flyer(request, company_id):
    try:
        company = Company.objects.get(public_id=company_id)
    except:
        raise Http404

    if company.is_company_user(request.user):
        if not company.flyer:
            generate_info_flyer_pdf(company)

        response = HttpResponse(company.flyer, content_type='application/pdf')
        response['Filename'] = company.flyer.name
        response['Content-Disposition'] = 'attachment; filename=%s' % company.flyer.name

        return response
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)