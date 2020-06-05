from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.urls import reverse

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration


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


def generate_info_flyer_pdf(request, company):

    data = {
        'company': company,
    }
    html_string = render_to_string('companies/company/pdf/info-flyer.html', request=request, context=data)
    css_string = render_to_string('companies/company/pdf/info-flyer.txt')

    pdf_title = "%s-flyer.pdf" % company.slug
    font_config = FontConfiguration()
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css = CSS(string=css_string, font_config=font_config)
    flyer_file = html.write_pdf(stylesheets=[css], font_config=font_config)
    pdf_file = ContentFile(flyer_file)
    company.flyer.save(pdf_title, pdf_file)
    url = "https://docs.google.com/gview?url=%s&embedded=true" % company.flyer.url
    response_data = {
        'previewUrl': url,
        'downloadUrl': reverse('download_company_flyer_api', args=[company.public_id, ])
    }
    return response_data
