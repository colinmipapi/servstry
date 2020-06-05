from django.core.exceptions import PermissionDenied
from companies.models import Company


def user_is_company_admin(function):

    def wrap(request, *args, **kwargs):
        if 'slug' in kwargs:
            company = Company.objects.get(slug=kwargs['slug'])
        else:
            company = Company.objects.none()

        if company.is_company_user(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap