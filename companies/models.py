import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.sites.shortcuts import get_current_site

from companies import storage_backends

from contact_trace.settings import GOOGLE_PLACES_API_KEY
from contact_trace.unique_slug import generate_unique_slug

from phonenumber_field.modelfields import PhoneNumberField

import phonenumbers
import googlemaps


STATES = (
        (None, '---'),
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
    )

SAFETY_POLICY_HELP_TEXT = {
    'B': 'A link to the safety policy is included below the guest contact information form. The guest agrees to the safety policy by submitting the form.',
    'CB': 'A link to your custom safety policy is included below the guest contact information form. The guest agrees to the safety policy by submitting the form.',
    'F': 'A checkbox is added to the guest contact information form with the text <b><i>"I have read and agree to the <a href="/safety-policy/">Safety Policy</a>"</i></b>. The guest is unable to submit the form until they check the box.',
    'CF': 'The same functionality as the standard form checkbox, except the safety policy links to your custom safety policy.',
    'P': 'A popup is displayed with the full text of the safety policy when the guest visits your profile. The guest must click the <b><i>"Agree"</i></b> button to interact with your profile and submit the form. If the guest clicks the <b><i>"Disagree"</i></b> button, they are redirected to <a href="https://coronavirus.dc.gov/">DC Government Coronavirus Homepage</a>.',
    'CP': 'The same functionality of the standard popup, but the Servstry Safety Policy is replaced by the text you provide.',
}


class Company(models.Model):

    STATUSES = (
        ('SU', 'Signing Up'),
        ('SB', 'Subscribed'),
        ('DL', 'Delinquent'),
        ('EP', 'Expiring'),
        ('CL', 'Canceled'),
        ('EX', 'Example')
    )
    SAFETY = (
        ('B', 'Basic'),
        ('CB', 'Custom Basic'),
        ('F', 'Form Checkbox'),
        ('CF', 'Custom Form Checkbox'),
        ('P', 'Popup'),
        ('CP', 'Custom Pop Up')
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        default=timezone.now,
    )
    status = models.CharField(
        max_length=2,
        choices=STATUSES,
        default='SU'
    )
    name = models.CharField(
        max_length=300,
        default=''
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )
    address1 = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    address2 = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    state = models.CharField(
        max_length=2,
        choices=STATES,
        null=True,
        blank=True
    )
    zip_code = models.CharField(
        max_length=5,
        null=True,
        blank=True
    )
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    place_id = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    website = models.URLField(
        null=True,
        blank=True
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        region='US'
    )
    safety_policy_setting = models.CharField(
        max_length=2,
        choices=SAFETY,
        default='B',
        verbose_name='Safety Policy Setting'
    )
    admins = models.ManyToManyField(
        'users.CustomUser',
        related_name='biz_admins',
        blank=True
    )
    # Media
    logo = models.FileField(
        storage=storage_backends.ProfileImageMediaStorage(),
        blank=True,
        null=True,
    )
    logo_background_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
    )
    cover_img = models.FileField(
        storage=storage_backends.CoverImageMediaStorage(),
        blank=True,
        null=True,
    )
    flyer = models.FileField(
        storage=storage_backends.FlyerMediaStorage(),
        blank=True,
        null=True,
    )
    # Stripe
    customer_id = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    trial_period = models.BooleanField(
        default=True
    )
    default_payment_method = models.OneToOneField(
        'billing.PaymentMethod',
        on_delete=models.CASCADE,
        related_name='company_default',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            pass
        else:  # create
            self.slug = generate_unique_slug(Company, self.name)

        super(Company, self).save(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse('company_profile', args=[self.slug])
        return url

    def get_simple_url(self):
        request = None
        return "".join([get_current_site(request).domain, self.get_absolute_url()])

    @property
    def get_full_url(self):
        request = None
        url = ''.join(['https://www.', get_current_site(request).domain, self.get_absolute_url()])
        return url

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        else:
            return static('media/imgs/placeholder-company.png')

    @property
    def get_cover_img_url(self):
        if self.cover_img:
            return self.cover_img.url
        else:
            return static('media/imgs/company-background.jpg')

    @property
    def get_flyer_preview_url(self):
        if self.flyer:
            url = "https://docs.google.com/gview?url=%s&embedded=true" % (self.flyer.url)
        else:
            url = ""
        return url

    @property
    def get_full_address(self):

        if self.address1:
            addr_str = self.address1
        else:
            return False

        if self.address2 and self.address2 != "":
            addr_str = "%s %s," % (addr_str, self.address2)
        else:
            addr_str = "%s," % (addr_str)
        if self.city:
            addr_str = "%s %s" % (addr_str, self.city)
        if self.state:
            addr_str = "%s, %s" % (addr_str, self.state)
        if self.zip_code:
            addr_str = "%s %s" % (addr_str, self.zip_code)

        return addr_str

    @property
    def phone_pretty(self):
        # Phone Field Formatted for Display
        if self.phone:
            p = phonenumbers.format_number(phonenumbers.parse(str(self.phone), 'US'),
                                           phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            p = None
        return p

    @property
    def website_pretty(self):
        # Website Field Formatted for Display
        if self.website:
            if 'http://' in self.website:
                website = self.website.replace('http://', '')
            elif 'https://' in self.website:
                website = self.website.replace('https://', '')
            else:
                website = self.website
            return website
        else:
            return None

    @property
    def get_gmaps_embed_url(self):
        url = "https://www.google.com/maps/embed/v1/place?key=%s&q=place_id:%s" % (GOOGLE_PLACES_API_KEY, self.place_id)
        return url

    def update_gmaps_data(self):

        gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
        place_q = gmaps.find_place(
            input=[self.name, self.get_full_address],
            input_type='textquery',
            fields=['name','geometry','place_id']
        )
        '''
        place_data = None
    
        if len(place_q['candidates']) > 1:
            for result in place_q['candidates']:
                if self.name == result['name']:
                    place_data = result
        else:
        '''

        try:
            place_data = place_q['candidates'][0]
        except:
            place_data = None

        if place_data == None:
            return "Error pulling new google maps data. Make sure the company name and address are correct."
        location = place_data['geometry']['location']
        self.lat = location['lat']
        self.lng = location['lng']
        self.place_id = place_data['place_id']

        self.save()

    def is_company_user(self, user):
        if user in self.admins.all() or user.is_superuser:
            return True
        else:
            return False


class WaitList(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    submitted = models.DateTimeField(
        default=timezone.now,
    )
    email = models.EmailField()

    def __str__(self):
        return self.email
