import json

from django.template.loader import render_to_string

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from billing.models import (
    PaymentMethod,
    Subscription
)
from companies.models import (
    Company,
)
from billing.backends import (
    create_or_update_subscription,
    create_or_update_payment_method,
    create_or_update_invoice
)

from contact_trace.settings import (
    DEBUG,
    STRIPE_LIVE_PUBLIC_KEY,
    STRIPE_TEST_PUBLIC_KEY,
    STRIPE_LIVE_SECRET_KEY,
    STRIPE_TEST_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET
)

import stripe

if DEBUG:
    stripe_public_key = STRIPE_TEST_PUBLIC_KEY
    stripe.api_key = STRIPE_TEST_SECRET_KEY

else:
    stripe_public_key = STRIPE_LIVE_PUBLIC_KEY
    stripe.api_key = STRIPE_LIVE_SECRET_KEY


@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
def check_coupon(request):

    try:
        data = stripe.Coupon.retrieve(request.POST.get('couponCode'))
        discount = data['amount_off'] / 100
        result = {
            'id': data['id'],
            'discount': discount
        }
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', ])
def create_subscription(request):
    data = request.data
    company = Company.objects.get(customer_id=data['customerId']['customerId'])
    if company.is_company_user(request.user):
        payment_method = stripe.PaymentMethod.attach(
            data['customerId']['paymentMethodId'],
            customer=data['customerId']['customerId'],
        )
        create_or_update_payment_method(payment_method, company=company)
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId']['customerId'],
            invoice_settings={
                'default_payment_method': data['customerId']['paymentMethodId'],
            },
        )

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=data['customerId']['customerId'],
            items=[
                {
                    'price': data['customerId']['priceId']
                }
            ],
            expand=['latest_invoice.payment_intent'],
            coupon=data['customerId']['couponId']
        )

        create_or_update_subscription(subscription, company=company)

        company.status = 'SB'
        company.save()
        return Response(subscription, status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def cancel_subscription(request, company_id):

    company = Company.objects.get(public_id=company_id)

    if company.is_company_user(request.user):
        data = request.data
        subscription_obj = Subscription.objects.get(stripe_id=data['subscriptionId'])
        try:
            subscription = stripe.Subscription.update(
                data['subscriptionId'],
                cancel_at_period_end=True
            )
        except Exception as e:
            subscription = stripe.Subscription.retrieve(data['subscriptionId'])
            create_or_update_payment_method(subscription, subscription_obj=subscription_obj)

        return Response({'status': 'success', 'subscription': subscription}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def retry_invoice(request):
    data = request.data
    try:
        stripe.PaymentMethod.attach(
            data['customerId']['paymentMethodId'],
            customer=data['customerId']['customerId'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId'],
            invoice_settings={
                'default_payment_method': data['customerId']['paymentMethodId'],
            },
        )

        invoice = stripe.Invoice.retrieve(
            data['customerId']['invoiceId'],
            expand=['customerId']['payment_intent'],
        )
        return Response(invoice, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def get_payment_method(request, payment_id):
    pass
    '''
        try:
            payment_method = stripe.PaymentMethod.retrieve(
                payment_id,
            )
            result = {
                'brand': payment_method['card']['brand'],
                'last4': payment_method['card']['last4']
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
    '''


@api_view(['POST', ])
def attach_payment_method(request):
    company = Company.objects.get(customer_id=request.data['customerId'])
    if company.is_company_user(request.user):
        payment_method = stripe.PaymentMethod.attach(
            request.data['paymentMethodId'],
            customer=request.data['customerId']
        )
        pm = create_or_update_payment_method(payment_method, company=company)
        context = {
            'payment': pm,
        }
        result = render_to_string('billing/snippets/payment-row-item.html', request=request, context=context)
        return Response(result, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT', ])
def change_default_payment_method(request, public_id):

    payment_method = PaymentMethod.objects.get(public_id=public_id)
    company = payment_method.company
    if company.is_company_user(request.user):
        stripe.Customer.modify(
            company.customer_id,
            invoice_settings={
                "default_payment_method": payment_method.stripe_id
            },
        )
        company.default_payment_method = payment_method
        company.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE', ])
def delete_payment_method(request, public_id):

    payment_method = PaymentMethod.objects.get(public_id=public_id)
    if payment_method.company.is_company_user(request.user):
        try:
            stripe.PaymentMethod.detach(
                payment_method.stripe_id,
            )
        except Exception as e:
            print('Delete Payment Method Error: %s' % str(e))
        payment_method.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
def stripe_webhook_recieved(request):

    webhook_secret = STRIPE_WEBHOOK_SECRET
    signature = request.headers.get('stripe-signature')

    if DEBUG:
        data = request.data['data']
        event_type = request.data['type']
    else:
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
            event_type = event['type']
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)

    if event_type == 'invoice.payment_succeeded':
        create_or_update_invoice(data['object'])

    if event_type == 'invoice.payment_failed':
        create_or_update_invoice(data['object'])

    if event_type == 'customer.subscription.created':
        create_or_update_subscription(data['object'], company=Company.objects.get(id=7))

    if event_type == 'customer.subscription.deleted':
        subscription = Subscription.objects.get(stripe_id=data['object']['id'])
        create_or_update_subscription(data['object'], subscription_obj=subscription)
        active_subscription = Subscription.objects.filter(
            company=subscription.company,
            status__in=['active', 'past_due', 'trailing', 'unpaid']
        )
        if not active_subscription:
            subscription.company.status = 'CL'
            subscription.company.save()
    if event_type == 'payment_method.attached':
        create_or_update_payment_method(data['object'])

    return Response({'status': 'success'})
