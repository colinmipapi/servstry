from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

from celery import Celery

from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contact_trace.settings')

app = Celery('contact_trace')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-subscription': {
        'task': 'billing.tasks.update_subscriptions',
        'schedule': crontab(minute=0, hour=0),
    },
    'update-plan': {
        'task': 'billing.tasks.update_plan',
        'schedule': crontab(minute=30, hour=0),
    },
    'update-coupon': {
        'task': 'billing.tasks.update_subscriptions',
        'schedule': crontab(minute=45, hour=0),
    },
    'update-payment-method': {
        'task': 'billing.tasks.update_payment_methods',
        'schedule': crontab(minute=0, hour=1),
    },
    'update-invoice': {
        'task': 'billing.tasks.update_invoices',
        'schedule': crontab(minute=0, hour=2),
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))