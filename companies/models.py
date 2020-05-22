import uuid

from django.db import models
from django.utils import timezone


class Company(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )


class WaitList(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    submitted = models.DateTimeField(
        default=timezone.now,
    )
    email = models.EmailField()
