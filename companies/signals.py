from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from datetime import timedelta

from companies.models import WaitList
from companies.tasks import (
    send_waitlist_email,
)


@receiver(post_save, sender=WaitList)
def new_waitlist(instance, created, **kwargs):
    '''
    if created:
        send_eta = timezone.now() + timedelta(minutes=15)
        send_waitlist_email.apply_async(
            [instance.id, ],
            eta=send_eta
        )
    '''