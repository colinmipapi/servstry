from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        assert request.user.is_authenticated
        url = reverse('settings', kwargs={'tab': 'social'})
        return url