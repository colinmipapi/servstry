from __future__ import absolute_import, unicode_literals

from contact_trace.celery import app

from track.models import GuestVisit
from track.backends import generate_confirmation_code_email


@app.task
def send_confirmation_code_email(guest_visit_id):
    guest_visit = GuestVisit.objects.get(id=guest_visit_id)
    generate_confirmation_code_email(guest_visit)
