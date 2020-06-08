import string
import random
import uuid

from django.db import models
from django.utils import timezone
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers


def confirmation_code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    code = ''.join(random.choice(chars) for _ in range(size))
    while GuestVisit.objects.filter(confirmation=code).exists():
        code = ''.join(random.choice(chars) for _ in range(size))
    return code


class GuestVisit(models.Model):

    # Computed Fields
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    submitted = models.DateTimeField(
        default=timezone.now,
    )
    confirmation = models.CharField(
        default=confirmation_code_generator,
        max_length=6
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    # Contact Info
    first_name = models.CharField(
        max_length=300,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=300,
        verbose_name='Last Name'
    )
    email = models.EmailField(
        verbose_name='E-mail Address'
    )
    phone = PhoneNumberField(
        verbose_name='Phone Number',
        region='US'
    )
    # User Model
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visits'
    )
    # Times
    arrival = models.DateTimeField(
        default=timezone.now,
    )
    departure = models.DateTimeField(
        null=True,
        blank=True
    )
    # Company
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='guest_visits'
    )

    def __str__(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        url = reverse('confirmation_page', args=[self.confirmation])
        return url

    @property
    def first_name_pretty(self):
        if self.user:
            return self.user.first_name
        else:
            return self.first_name

    @property
    def last_name_pretty(self):
        if self.user:
            return self.user.last_name
        else:
            return self.last_name

    @property
    def get_full_name(self):
        if self.user:
            return self.user.get_full_name
        else:
            return "%s %s" % (self.first_name, self.last_name)

    @property
    def email_pretty(self):
        if self.user:
            return self.user.email
        else:
            return self.email

    @property
    def phone_pretty(self):
        # Phone Field Formatted for Display
        if self.user:
            p = self.user.phone_pretty
        elif self.phone:
            p = phonenumbers.format_number(phonenumbers.parse(str(self.phone), 'US'),
                                           phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            p = None
        return p

    @property
    def arrival_pretty(self):
        arrival = timezone.localtime(self.arrival)
        return arrival.strftime("%m/%d/%y %I:%M %p")

    @property
    def arrival_date_pretty(self):
        return self.arrival.strftime("%m/%d/%y")

    @property
    def arrival_time_pretty(self):
        return self.arrival.strftime("%I:%M %p")

    def add_user_information(self, user):
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.phone = user.phone
        self.email = user.email
        self.save()


class CustomSafetyPolicy(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        default=timezone.now,
    )
    company = models.OneToOneField(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='safety_policy'
    )
    policy_text = models.TextField()

    def __str__(self):
        return "%s" % self.company.name
