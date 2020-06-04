from datetime import datetime

from django.utils import timezone
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


def create_or_update_plan(plan, **kwargs):

    plan_obj, new = Plan.objects.update_or_create(
        stripe_id=plan['id'],
        created=make_aware(datetime.fromtimestamp(plan['created'])),
        active=plan['active'],
        price=plan['amount'],
        interval=plan['interval'],
    )

    plan_obj.last_updated=timezone.now()
    plan_obj.save()

    return plan_obj


def retrieve_plan(plan_stripe_id):
    return stripe.Plan.retrieve(plan_stripe_id)


def create_or_update_subscription(subscription, **kwargs):

    if 'company' in kwargs:
        company = kwargs['company']
    else:
        company = Company.objects.get(customer_id=subscription['customer'])

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

    if subscription['next_pending_invoice_item_invoice']:
        next_pending_invoice = make_aware(datetime.fromtimestamp(subscription['next_pending_invoice_item_invoice']))
    else:
        next_pending_invoice = None

    if subscription['canceled_at']:
        canceled_at = make_aware(datetime.fromtimestamp(subscription['canceled_at']))
    else:
        canceled_at = None

    if subscription['cancel_at']:
        cancel_at = make_aware(datetime.fromtimestamp(subscription['cancel_at']))
    else:
        cancel_at = None

    if 'subscription_obj' in kwargs:
        sub = kwargs['subscription_obj']
        sub.status = subscription['status']
        sub.current_period_end = make_aware(datetime.fromtimestamp(subscription['current_period_end']))
        sub.next_pending_invoice = next_pending_invoice
        sub.canceled_at = canceled_at
        sub.cancel_at = cancel_at
        sub.last_updated = timezone.now()

    else:
        sub, new = Subscription.objects.update_or_create(
            stripe_id=subscription['id'],
            created=make_aware(datetime.fromtimestamp(subscription['created'])),
            status=subscription['status'],
            company=company,
            plan=plan,
            discount=discount,
            current_period_end=make_aware(datetime.fromtimestamp(subscription['current_period_end'])),
            next_pending_invoice=next_pending_invoice,
            canceled_at=canceled_at,
            cancel_at=cancel_at,
        )

    sub.last_updated = timezone.now()
    sub.save()

    return sub


def retrieve_subscription(sub_stripe_id):
    return stripe.Subscription.retrieve(sub_stripe_id)


def create_or_update_payment_method(payment_method, **kwargs):

    if 'company' in kwargs:
        company = kwargs['company']
    else:
        company = Company.objects.get(customer_id=payment_method['customer'])

    pm, new = PaymentMethod.objects.update_or_create(
        stripe_id=payment_method['id'],
        created=make_aware(datetime.fromtimestamp(payment_method['created'])),
        company=company,
        brand=payment_method['card']['brand'],
        last4=payment_method['card']['last4'],
        exp_month=payment_method['card']['exp_month'],
        exp_year=payment_method['card']['exp_year'],
    )

    pm.last_updated = timezone.now()
    pm.save()

    if not company.cards.all().exists():
        company.default_payment_method = pm
        company.save()

    return pm


def retrieve_payment_method(payment_method_stripe_id):
    return stripe.PaymentMethod.retrieve(payment_method_stripe_id)


def create_or_update_invoice(invoice, **kwargs):
    if 'company' in kwargs:
        company = kwargs['company']
    else:
        company = Company.objects.get(customer_id=invoice['customer'])

    if 'subscription' in kwargs:
        subscription = kwargs['subscription']
    else:
        try:
            subscription = Subscription.objects.get(stripe_id=invoice['subscription'])
        except:
            subscription = retrieve_subscription(invoice['subscription'])

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
        paid_at=paid_at,

    )
    inv.last_updated = timezone.now()
    inv.save()

    return inv


def retrieve_invoice(invoice_stripe_id):
    return stripe.Invoice.retrieve(invoice_stripe_id)


def create_or_update_coupon(coupon, **kwargs):

    coupon_obj, new = Coupon.objects.update_or_create(
        stripe_id=coupon['id'],
        created=make_aware(datetime.fromtimestamp(coupon['created'])),
        discount=coupon['amount_off'],
        duration=coupon['duration'],
        duration_in_months=coupon['duration_in_months'],
    )

    coupon_obj.name = coupon['name']
    coupon_obj.last_updated = timezone.now()
    coupon_obj.save()
    return coupon_obj


def retrieve_coupon(coupon_stripe_id):
    return stripe.Coupon.retrieve(coupon_stripe_id)
