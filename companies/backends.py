from django.core.mail import send_mail
from django.template.loader import render_to_string


def generate_waitlist_email(waitlist):
    subject = ""
    html_message = render_to_string('company/emails/html/waitlist_email.html', {

    })
    plain_message = render_to_string('company/emails/txt/waitlist_email.txt', {

    })
    send_mail(
        subject,
        plain_message,
        'Servstry <notifications@servstry.com>',
        [waitlist.email, ],
        html_message=html_message
    )