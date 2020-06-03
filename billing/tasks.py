from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from contact_trace.celery import app

from billing.models import (
    Subscription,
    Plan,
    Coupon,
    PaymentMethod,
    Invoice
)
from billing.backends import (
    retrieve_subscription,
    create_or_update_subscription,
    retrieve_plan,
    create_or_update_plan,
    retrieve_coupon,
    create_or_update_coupon,
    retrieve_payment_method,
    create_or_update_payment_method,
    retrieve_invoice,
    create_or_update_invoice
)


@app.task
def update_subscriptions():
    time_range = timezone.now() - timedelta(days=7)
    subscriptions = Subscription.objects.filter(
        Q(last_updated__isnull=True) | Q(last_updated__lte=time_range)
    ).filter(status__in=['active', 'trailing', 'past_due', 'unpaid'])
    for sub in subscriptions:
        subscription = retrieve_subscription(sub.stripe_id)
        create_or_update_subscription(subscription, subscription_obj=sub)


@app.task
def update_plans():
    time_range = timezone.now() - timedelta(days=7)
    plans = Plan.objects.filter(
        Q(last_updated__isnull=True) | Q(last_updated__lte=time_range)
    ).filter(active=True)
    for plan_obj in plans:
        plan = retrieve_plan(plan_obj.stripe_id)
        create_or_update_plan(plan, plan_obj=plan_obj)


@app.task
def update_coupons():
    time_range = timezone.now() - timedelta(days=7)
    coupons = Coupon.objects.filter(
        Q(last_updated__isnull=True) | Q(last_updated__lte=time_range)
    )
    for coupon_obj in coupons:
        coupon = retrieve_coupon(coupon_obj.stripe_id)
        create_or_update_coupon(coupon, coupon_obj=coupon_obj)


@app.task
def update_payment_methods():
    time_range = timezone.now() - timedelta(days=7)
    payment_methods = PaymentMethod.objects.filter(
        Q(last_updated__isnull=True) | Q(last_updated__lte=time_range)
    )
    for pm in payment_methods:
        payment_method = retrieve_payment_method(pm.stripe_id)
        create_or_update_payment_method(payment_method)


@app.task
def update_invoices():
    time_range = timezone.now() - timedelta(days=7)
    invoices = Invoice.objects.filter(
        Q(last_updated__isnull=True) | Q(last_updated__lte=time_range)
    ).exclude(status__in=['paid', 'void'])
    for invoice_obj in invoices:
        invoice = retrieve_invoice(invoice_obj.stripe_id)
        create_or_update_invoice(invoice)
