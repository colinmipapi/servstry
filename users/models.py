import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


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
