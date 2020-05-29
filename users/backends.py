from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

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
            'Servstry <notifications@servstry.com>',
            recipients,
        )


def generate_user_invite_email(invitation):
    request = None
    accept_url = ''.join(['https://www.', get_current_site(request).domain, invitation.get_absolute_url()])

    w_subject = "%s added you as an admin on Servstry" % invitation.inviter.name
    message = '%s added you as an admin on Servstry. Create a profile to view and manage guest visits.' % invitation.inviter.name

    message_dict = {
        'sender': {
            'name': invitation.inviter.name,
        },
        'to_user': {
            'name': invitation.user.first_name,
        },
        'message': message,
        'accept_url': accept_url
    }

    html_message = render_to_string('users/emails/html/send_invite.html', message_dict)
    plain_message = render_to_string('users/emails/txt/send_invite.txt', message_dict)
    send_mail(
        w_subject,
        plain_message,
        'Servstry <notifications@servstry.com>',
        [invitation.user.email, ],
        html_message=html_message
    )