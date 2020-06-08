from __future__ import absolute_import, unicode_literals

from contact_trace.celery import app

from users.models import Invitation
from users.backends import generate_user_invite_email


@app.task
def send_user_invite_email(invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    generate_user_invite_email(invitation)
