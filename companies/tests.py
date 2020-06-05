from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from companies.models import Company
from users.models import CustomUser

from companies import views

from allauth.socialaccount.models import SocialApp

client = Client()


class CompanyTestCase(TestCase):

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
        user3 = CustomUser.objects.create_user(
            first_name='Peter',
            last_name='Taylor',
            email='peter@taylor.com',
            password='secret',
            username='peter'
        )

        # Company in the Sign Up Process
        su_company = Company.objects.create(
            status='SU',
            name="Fake Burger",
            address1="3 Pine Lane",
            city="Bayville",
            state="NY",
            zip_code="11709",
            website="https://www.ndustrylink.com",
            phone="5165245372",
        )
        su_company.admins.add(user1)

        # Company Fully Subscribed
        sb_company = Company.objects.create(
            status='SB',
            name="Fake Cocktail",
            address1="27 Ledyard Rd",
            city="Winchester",
            state="MA",
            zip_code="01890",
            website="https://www.fakecocktail.com",
            phone="5165245362",
        )
        sb_company.admins.add(user2)

        # Company with a failed payment method
        dl_company = Company.objects.create(
            status='DL',
            name="Not Fake Cocktail",
            address1="26 Ledyard Rd",
            city="Winchester",
            state="MA",
            zip_code="01890",
            website="https://www.notfakecocktail.com",
            phone="5165245262",
        )
        dl_company.admins.add(user1)

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

    # Sign Up Views
    def test_create_company_name_address(self):
        self.client.login(username='peter', password='secret')
        url = reverse('create_company_name_address')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_post_create_company_name_address(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        user = CustomUser.objects.get(email="peter@taylor.com")
        form_data = {
            'name': 'The Pineapple Club',
            'address1': '1428 Montello Ave NE',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20002'
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("create_company_name_address"),
            form_data,
        )
        request.user = user
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.create_company_name_address(request)
        self.assertEqual(response.status_code, 302)

    def test_create_contact_info(self):
        self.client.login(username='peter', password='secret')
        url = reverse('create_company_name_address')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_post_create_contact_info(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        user = CustomUser.objects.get(email="janedoe@fake.com")
        form_data = {
            'website': "https://www.fakecocktail.com",
            'phone': "(516) 524-5362"
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("create_contact_info"),
            form_data,
        )
        request.user = user
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.create_contact_info(request)
        self.assertEqual(response.status_code, 302)

    def test_create_invite_admins(self):
        self.client.login(username='janedoe', password='secret')
        url = reverse('create_invite_admins')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_create_payment(self):
        self.client.login(username='janedoe', password='secret')
        url = reverse('create_payment')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Profile Views
    def test_company_profile_anon_user_company_su(self):
        company = Company.objects.get(name="Fake Burger")
        url = reverse('company_profile', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_company_profile_anon_user_company_sb(self):
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse('company_profile', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_company_profile_anon_user_company_dl(self):
        company = Company.objects.get(name="Not Fake Cocktail")
        url = reverse('company_profile', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_company_profile_admin_user(self):
        self.client.login(username='johndoe', password='secret')
        company = Company.objects.get(name="Fake Burger")
        url = reverse('company_profile', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_company_profile_anon_post_guest_visit_form(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        company = Company.objects.get(name="Fake Cocktail")
        form_data = {
            'first_name': 'Jack',
            'last_name': 'Bauer',
            'email': 'jack@bauer.com',
            'phone': '(516) 524-5362',
            'arrival': '6/12/20 8:00 pm'
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("company_profile", args=[company.slug, ]),
            form_data,
        )
        request.user = AnonymousUser()
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.company_profile(request, company.slug)
        self.assertEqual(response.status_code, 302)

    # Dashboard Views
    def test_company_dashboard(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse('company_dashboard', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_company_dashboard_anon(self):
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse('company_dashboard', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_post_company_dashboard(self):
        session_middleware = SessionMiddleware()
        message_middleware = MessageMiddleware()
        company = Company.objects.get(name="Fake Cocktail")
        form_data = {
            'start_filter': '5/12/20 8:00 pm',
            'end_filter': '6/12/20 8:00 pm'
        }
        rf = RequestFactory()
        request = rf.post(
            reverse("company_dashboard", args=[company.slug, ]),
            form_data,
        )
        request.user = CustomUser.objects.get(username='janedoe')
        session_middleware.process_request(request)
        request.session.save()
        message_middleware.process_request(request)
        request.session.save()
        response = views.company_dashboard(request, slug=company.slug)
        self.assertEqual(response.status_code, 200)

    def test_new_subscription(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse('new_subscription', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_settings(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse('company_settings', args=[company.slug, ])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_settings_personal(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse(
            'company_settings_tab',
            kwargs={
                'slug': company.slug,
                'tab': 'personal',
            })
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_settings_company(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse(
            'company_settings_tab',
            kwargs={
                'slug': company.slug,
                'tab': 'company',
            })
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_settings_admins(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse(
            'company_settings_tab',
            kwargs={
                'slug': company.slug,
                'tab': 'admins',
            })
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_settings_payment(self):
        self.client.login(username='janedoe', password='secret')
        company = Company.objects.get(name="Fake Cocktail")
        url = reverse(
            'company_settings_tab',
            kwargs={
                'slug': company.slug,
                'tab': 'payment',
            })
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)