import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey

from phonenumber_field.modelfields import PhoneNumberField

import phonenumbers


class CustomUser(AbstractUser):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        region='US'
    )

    @property
    def phone_pretty(self):
        # Phone Field Formatted for Display
        if self.phone:
            p = phonenumbers.format_number(phonenumbers.parse(str(self.phone), 'US'),
                                           phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            p = None
        return p


class Invitation(models.Model):

    TYPES = (
        ('C', 'Company User'),
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        default=timezone.now,
    )
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='user_invitations'
    )
    invitation_type = models.CharField(
        max_length=2,
        choices=TYPES,
        blank=True,
        null=True
    )
    inviter_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    inviter_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    inviter = GenericForeignKey(
        'inviter_content_type',
        'inviter_object_id'
    )

    def __str__(self):
        return str(self.public_id)

    def get_absolute_url(self):
        url = reverse('invitation_signup', args=[self.public_id])
        return url