from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from companies.models import (
    Company,
)

from contact_trace.settings import (
    DEBUG,
    STRIPE_LIVE_PUBLIC_KEY,
    STRIPE_TEST_PUBLIC_KEY,
    STRIPE_LIVE_SECRET_KEY,
    STRIPE_TEST_SECRET_KEY
)

import stripe

if DEBUG:
    stripe_public_key = STRIPE_TEST_PUBLIC_KEY
    stripe.api_key = STRIPE_TEST_SECRET_KEY

else:
    stripe_public_key = STRIPE_LIVE_PUBLIC_KEY
    stripe.api_key = STRIPE_LIVE_SECRET_KEY


@api_view(['POST', ])
def create_subscription(request):
    data = request.data
    company = Company.objects.get(customer_id=data['customerId']['customerId'])
    if company.is_company_user(request.user):
        stripe.PaymentMethod.attach(
            data['customerId']['paymentMethodId'],
            customer=data['customerId']['customerId'],
        )
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
        )
        company.status = 'SB'
        company.save()
        return Response(subscription, status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)