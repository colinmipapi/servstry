from django.urls import path

from billing import api_views as views

urlpatterns = [
    path(
        'stripe-webhook/',
        views.stripe_webhook_recieved,
        name='stripe-webhook-recieved'
    ),
    path(
        'check-coupon/',
        views.check_coupon,
        name='check-coupon'
    ),
    path(
        'create-subscription/',
        views.create_subscription,
        name='create-subscription'
    ),
    path(
        'cancel-subscription/<uuid:company_id>/',
        views.cancel_subscription,
        name='cancel-subscription'
    ),
    path(
        'retry-invoice/',
        views.retry_invoice,
        name='retry-invoice'
    ),
    path(
        'get-payment-method/<str:payment_id>/',
        views.get_payment_method,
        name='get-payment-method'
    ),
    path(
        'attach-payment-method/',
        views.attach_payment_method,
        name='attach-payment-method'
    ),
    path(
        'change-default-payment-method/<uuid:public_id>/',
        views.change_default_payment_method,
        name='change-default-payment-method'
    ),
    path(
        'delete-payment-method/<uuid:public_id>/',
        views.delete_payment_method,
        name='delete-payment-method'
    ),
]
