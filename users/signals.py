from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission

from users.models import CustomUser, Invitation
from users.tasks import send_user_invite_email


@receiver(post_save, sender=CustomUser)
def add_company_permission(instance, **kwargs):

    permission = Permission.objects.get(name='Can add company')

    if permission not in instance.user_permissions.all():
        instance.user_permissions.add(permission)


@receiver(post_save, sender=Invitation)
def new_invitation(sender, instance, created, **kwargs):
    if created:
        send_user_invite_email.apply_async([instance.id, ])