from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.contenttypes.models import ContentType

from companies.models import Company
from users.models import (
    CustomUser,
    Invitation
)

from users import views

from allauth.socialaccount.models import SocialApp

client = Client()


class UserTestCase(TestCase):

    def setUp(self):

        self.current_site = Site.objects.get_current()

        user1 = CustomUser.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@fake.com",
            password="secret",
            phone="5165245372",
            username='whatever'
        )
        user2 = CustomUser.objects.create_user(
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

        self.invitation = Invitation.objects.create(
            email="janedoe@fake.com",
            user=user2,
            invitation_type='C',
            inviter_content_type=ContentType.objects.get_for_model(company),
            inviter_object_id=company.id
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

    def test_home_anon(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_home_auth(self):
        self.client.login(username='whatever', password='secret')
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_business_landing(self):
        url = reverse('business_landing')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_landing(self):
        url = reverse('landing')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_invitation_signup(self):
        url = reverse('invitation_signup', args=[self.invitation.public_id, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_invitation_signup_post(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@fake.com',
            'phone': '2165245372',
            'password1': 'ErY7u4!yt',
            'password2': 'ErY7u4!yt'
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("invitation_signup", args=[self.invitation.public_id, ]),
            form_data,
        )
        request.user = AnonymousUser()
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.invitation_signup(request, invitation_id=self.invitation.public_id)
        self.assertEqual(response.status_code, 302)

    def test_contact_us(self):
        url = reverse('contact_us')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_post_contact_us(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        form_data = {
            'full_name': 'Jack Bauer',
            'email_address': 'jack@bauer.com',
            'message': 'test message'
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("contact_us"),
            form_data,
        )
        request.user = AnonymousUser()
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.contact_us(request)
        self.assertEqual(response.status_code, 200)

    def test_user_contact_info(self):
        self.client.login(username='whatever', password='secret')
        url = reverse('user-contact-info')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_contact_info_post(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        form_data = {
            'first_name': 'Jack',
            'last_name': 'Bauer',
            'phone': '(516) 524-5362',
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("user-contact-info"),
            form_data,
        )
        request.user = CustomUser.objects.get(username='whatever')
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.user_contact_info(request)
        self.assertEqual(response.status_code, 302)