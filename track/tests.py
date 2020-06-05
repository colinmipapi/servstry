from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.urls import reverse

from companies.models import Company
from track.models import GuestVisit
from users.models import CustomUser

from track import views

from allauth.socialaccount.models import SocialApp

client = Client()


class TrackTestCase(TestCase):

    def setUp(self):

        self.current_site = Site.objects.get_current()

        user = CustomUser.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@fake.com",
            username="janedoe",
            password="secret",
            phone="2165245372",
        )

        company = Company.objects.create(
            status='SB',
            name="Fake Cocktail",
            address1="27 Ledyard Rd",
            city="Winchester",
            state="MA",
            zip_code="01890",
            website="https://www.fakecocktail.com",
            phone="5165245362",
        )
        company.admins.add(user)

        GuestVisit.objects.create(
            first_name='Peter',
            last_name='Taylor',
            email='peter@taylor.com',
            phone="5165245372",
            company=company
        )

        google = SocialApp.objects.create(
            provider="Google",
            name="google",
            secret="blank",
            client_id="blank",
        )
        google.sites.add(self.current_site)
        facebook = SocialApp.objects.create(
            provider="facebook",
            name="facebook",
            client_id="1234567890",
            secret="0987654321",
        )
        facebook.sites.add(self.current_site)

    def test_confirmation_page(self):

        gv = GuestVisit.objects.get(email='peter@taylor.com')
        url = reverse('confirmation_page', args=[gv.confirmation, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
