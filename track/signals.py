from django.dispatch import receiver
from django.db.models.signals import post_save

from track.models import GuestVisit

from track.tasks import send_confirmation_code_email


@receiver(post_save, sender=GuestVisit)
def send_confirmation_email(instance, created, **kwargs):

    if created:
        if instance.user:
            if instance.user.email_setting:
                send = True
            else:
                send = False
        else:
            send = True

        if send:
            send_confirmation_code_email.apply_async([instance.id, ])
