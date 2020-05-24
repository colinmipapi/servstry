from django.core.mail import send_mail
from django.contrib.sites.models import Site

from users.models import CustomUser


def get_admin_recipients():
    current_site = Site.objects.get_current()
    if current_site.domain != 'example.com':
        recipients = list(CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True))
        return recipients
    else:
        return False


def demo_request_email(data):
    recipients = get_admin_recipients()
    if recipients:
        subject = 'New Demo Request'
        email_text = "Demo Request \r\n Name: %s \r\n Email: %s \r\n Phone: %s \r\n Company: %s" % (
            data.name,
            data.email,
            data.phone,
            data.company
        )
        send_mail(
            subject,
            email_text,
            '',
            recipients,
        )
