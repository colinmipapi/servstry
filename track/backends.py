from django.core.mail import send_mail
from django.template.loader import render_to_string


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_confirmation_code_email(guest_visit):

    subject = "Entry Confirmation For %s" % guest_visit.company.name
    html = render_to_string('track/emails/html/confirmation_code.html', {
        'guest_visit': guest_visit,
    })
    text = render_to_string('track/emails/txt/confirmation_code.txt', {
        'guest_visit': guest_visit,
    })
    send_mail(
        subject,
        text,
        '',
        [guest_visit.email, ],
        html_message=html
    )
