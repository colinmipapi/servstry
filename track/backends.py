import csv
import xlwt
from io import StringIO, BytesIO

from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
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


def generate_csv_report_email(guest_visits, to_user):

    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([
        'First Name',
        'Last Name',
        'E-mail',
        'Phone',
        'Arrival Date',
        'Arrival Time',
        'Code'
    ])
    for guest in guest_visits:
        csv_writer.writerow([
            guest.first_name,
            guest.last_name,
            guest.email,
            guest.phone_pretty,
            guest.arrival_date_pretty,
            guest.arrival_time_pretty,
            guest.confirmation
        ])

    date = timezone.now().strftime('%m/%d/%Y %I:%M %p')

    subject = "Your Report is Ready - %s" % date
    text = render_to_string('track/emails/txt/report_ready.txt', {
        'user': to_user,
    })

    message = EmailMessage(
        subject,
        text,
        '',
        [to_user.email, ]
    )
    message.attach('report.csv', csv_file.getvalue(), 'text/csv')
    message.send()


def generate_xls_report_email(guest_visits, to_user):

    f = BytesIO()

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Guest Visits')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        'First Name',
        'Last Name',
        'E-mail',
        'Phone',
        'Arrival Date',
        'Arrival Time',
        'Code'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for guest in guest_visits:

        row = [
            guest.first_name,
            guest.last_name,
            guest.email,
            guest.phone_pretty,
            guest.arrival_date_pretty,
            guest.arrival_time_pretty,
            guest.confirmation
        ]

        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(f)

    date = timezone.now().strftime('%m/%d/%Y %I:%M %p')

    subject = "Your Report is Ready - %s" % date
    text = render_to_string('track/emails/txt/report_ready.txt', {
        'user': to_user,
    })

    message = EmailMessage(
        subject,
        text,
        '',
        [to_user.email, ]
    )
    message.attach('report.xls', f.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    message.send()
