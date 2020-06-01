from datetime import datetime

from django.utils.timezone import make_aware

from billing.models import (
    Subscription,
    Plan,
    PaymentMethod,
    Coupon,
    Invoice
)
from companies.models import (
    Company
)

from contact_trace.settings import (
    DEBUG,
    STRIPE_LIVE_PUBLIC_KEY,
    STRIPE_TEST_PUBLIC_KEY,
    STRIPE_LIVE_SECRET_KEY,
    STRIPE_TEST_SECRET_KEY,
)

import stripe

if DEBUG:
    stripe_public_key = STRIPE_TEST_PUBLIC_KEY
    stripe.api_key = STRIPE_TEST_SECRET_KEY

else:
    stripe_public_key = STRIPE_LIVE_PUBLIC_KEY
    stripe.api_key = STRIPE_LIVE_SECRET_KEY


def subscription_lookup(subscription_id):

    sub = stripe.Subscription.retrieve("sub_HNUFr4y5Y6cRFo")

    return sub


def create_or_update_plan(plan, **kwargs):

    plan_obj, new = Plan.objects.update_or_create(
        stripe_id=plan['id'],
        created=make_aware(datetime.fromtimestamp(plan['created'])),
        active=plan['active'],
        price=plan['amount'],
        interval=plan['interval']
    )

    return plan_obj


def create_or_update_subscription(subscription, **kwargs):
    print(subscription['customer'])
    if 'company' in kwargs:
        company = kwargs['company']
    else:
        try:
            company = Company.objects.get(customer_id=subscription['customer'])
        except:
            company = Company.objects.get(id=7)

    try:
        plan = Plan.objects.get(stripe_id=subscription['items']['data'][0]['plan']['id'])
    except:
        plan = create_or_update_plan(subscription['items']['data'][0]['plan'])

    if subscription['discount']:
        try:
            discount = Coupon.objects.get(stripe_id=subscription['discount']['coupon']['id'])
        except:
            discount = create_or_update_coupon(subscription['discount']['coupon'])
    else:
        discount = None

    sub, new = Subscription.objects.update_or_create(
        stripe_id=subscription['id'],
        created=make_aware(datetime.fromtimestamp(subscription['created'])),
        status=subscription['status'],
        company=company,
        plan=plan,
        discount=discount,
        next_pending_invoice=subscription['next_pending_invoice_item_invoice']
    )

    return sub


def create_or_update_payment_method(payment_method, **kwargs):

    if 'company' in kwargs:
        company = kwargs['company']
    else:
        try:
            company = Company.objects.get(customer_id=payment_method['customer'])
        except:
            company = Company.objects.get(id=7)

    pm, new = PaymentMethod.objects.update_or_create(
        stripe_id=payment_method['id'],
        created=make_aware(datetime.fromtimestamp(payment_method['created'])),
        company=company,
        brand=payment_method['card']['brand'],
        last4=payment_method['card']['last4'],
        exp_month=payment_method['card']['exp_month'],
        exp_year=payment_method['card']['exp_year'],
    )

    if company.cards.all().exists():
        company.default_payment_method = pm
        company.save()

    return pm


def create_or_update_invoice(invoice, **kwargs):
    if 'company' in kwargs:
        company = kwargs['company']
    else:
        try:
            company = Company.objects.get(customer_id=invoice['customer'])
        except:
            company = Company.objects.get(id=7)

    if 'subscription' in kwargs:
        subscription = kwargs['subscription']
    else:
        try:
            subscription = Subscription.objects.get(stripe_id=invoice['subscription'])
        except:
            subscription = subscription_lookup(invoice['subscription'])

    if invoice['status_transitions']['paid_at']:
        paid_at = make_aware(datetime.fromtimestamp(invoice['status_transitions']['paid_at']))
    else:
        paid_at = None

    inv, new = Invoice.objects.update_or_create(
        stripe_id=invoice['id'],
        created=make_aware(datetime.fromtimestamp(invoice['created'])),
        company=company,
        subscription=subscription,
        pdf_url=invoice['invoice_pdf'],
        hosted_invoice_url=invoice['hosted_invoice_url'],
        status=invoice['status'],
        period_start=make_aware(datetime.fromtimestamp(invoice['period_start'])),
        period_end=make_aware(datetime.fromtimestamp(invoice['period_end'])),
        amount_due=invoice['amount_due'],
        amount_paid=invoice['amount_paid'],
        paid_at=paid_at
    )

    return inv


def create_or_update_coupon(coupon, **kwargs):

    coupon, new = Coupon.objects.update_or_create(
        stripe_id=coupon['id'],
        created=make_aware(datetime.fromtimestamp(coupon['created'])),
        discount=coupon['amount_off'],
        duration=coupon['duration'],
        duration_in_months=coupon['duration_in_months']
    )

    return coupon
