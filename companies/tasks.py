from __future__ import absolute_import, unicode_literals

from contact_trace.celery import app

from companies.models import WaitList
from companies.backends import generate_waitlist_email


@app.task
def send_waitlist_email(waitlist_id):
    waitlist = WaitList.objects.get(id=waitlist_id)
    generate_waitlist_email(waitlist)