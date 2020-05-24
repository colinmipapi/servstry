from django.dispatch import receiver
from django.db.models.signals import post_save

from track.models import GuestVisit

from track.tasks import send_confirmation_code_email


@receiver(post_save, sender=GuestVisit)
def add_company_permission(instance, created, **kwargs):

    if created:
        send_confirmation_code_email.apply_async([instance.id, ])
