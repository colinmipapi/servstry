from __future__ import absolute_import, unicode_literals

from contact_trace.celery import app

from users.models import (
    CustomUser,
)

from companies.models import (
    Company,
)

from track.models import GuestVisit
from track.backends import (
    generate_confirmation_code_email,
    generate_csv_report_email,
    generate_xls_report_email
)


@app.task
def send_confirmation_code_email(guest_visit_id):
    guest_visit = GuestVisit.objects.get(id=guest_visit_id)
    generate_confirmation_code_email(guest_visit)


@app.task
def send_report_email(company_id, to_user_id, file_type, start, end):

    company = Company.objects.get(id=company_id)
    to_user = CustomUser.objects.get(
        id=to_user_id
    )

    guests = GuestVisit.objects.filter(
        company=company
    ).order_by('-arrival')

    if start:
        guests.filter(arrival__gte=start)
    if end:
        guests.filter(arrival__lte=end)

    if file_type == 'C':
        generate_csv_report_email(guests, to_user)
    elif file_type == 'X':
        generate_xls_report_email(guests, to_user)