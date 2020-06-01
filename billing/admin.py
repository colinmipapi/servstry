from django.contrib import admin
from billing.models import (
    Subscription,
    Plan,
    Coupon,
    PaymentMethod,
    Invoice
)


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription


class PlanAdmin(admin.ModelAdmin):
    model = Plan


class CouponAdmin(admin.ModelAdmin):
    model = Coupon


class PaymentMethodAdmin(admin.ModelAdmin):
    model = PaymentMethod


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Invoice, InvoiceAdmin)
