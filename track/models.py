import string
import random
import uuid

from django.db import models
from django.utils import timezone

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
        return "%s %s" % (self.first_name, self.last_name)

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
    def get_full_name(self):

        return "%s %s" % (self.first_name, self.last_name)
