from django.db import models
from django.templatetags.static import static


class Subscription(models.Model):

    STATUSES = (
        ('incomplete', 'Incomplete'),
        ('incomplete_expired', 'Incomplete Expired'),
        ('trialing', 'Trailing'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid')
    )

    stripe_id = models.CharField(
        max_length=150,
        unique=True,
    )
    created = models.DateTimeField()
    status = models.CharField(
        max_length=25,
        choices=STATUSES
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(
        'billing.Plan',
        on_delete=models.CASCADE
    )
    discount = models.ForeignKey(
        'billing.Coupon',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    next_pending_invoice = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.company.name

    @property
    def real_price(self):
        if self.discount:
            final_price = (self.plan.price - self.discount) / 100
        else:
            final_price = self.plan.price / 100

        real_price = "$%s" % "{:.2f}".format(final_price)

        return real_price


class Plan(models.Model):

    INTERVALS = (
        ('day', 'Daily'),
        ('week', 'Weekly'),
        ('month', 'Monthly'),
        ('year', 'Yearly')
    )

    stripe_id = models.CharField(
        max_length=150,
        unique=True,
    )
    created = models.DateTimeField()
    active = models.BooleanField()
    price = models.PositiveIntegerField()
    interval = models.CharField(
        max_length=25,
        choices=INTERVALS
    )

    def __str__(self):
        price = "$%s" % "{:.2f}".format((self.price / 100))
        return "%s %s" % (price, self.get_interval_display())


class Coupon(models.Model):

    DURATIONS = (
        ('once', 'Once'),
        ('recurring', 'Recurring'),
        ('forever', 'Forever')
    )

    stripe_id = models.CharField(
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        max_length=300,
    )
    created = models.DateTimeField()
    discount = models.PositiveIntegerField()
    duration = models.CharField(
        max_length=25,
        choices=DURATIONS
    )
    duration_in_months = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):

    BRANDS = (
        ('amex', 'American Express'),
        ('diners', 'Diners Club'),
        ('discover', 'Discover'),
        ('jcb', 'JCB'),
        ('mastercard', 'MasterCard'),
        ('unionpay', 'UnionPay'),
        ('visa', 'Visa'),
        ('unknown', 'Unknown')
    )

    stripe_id = models.CharField(
        max_length=150,
        unique=True,
    )
    created = models.DateTimeField()
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='cards'
    )
    brand = models.CharField(
        max_length=25,
        choices=BRANDS
    )
    last4 = models.CharField(
        max_length=4,
    )
    exp_month = models.CharField(
        max_length=2,
    )
    exp_year = models.CharField(
        max_length=4,
    )

    def __str__(self):
        return "%s (%s %s)" % (self.company.name, self.get_brand_display(), self.last4)

    @property
    def get_icon_path(self):
        if self.brand in ['unionpay', 'unknown']:
            path = 'icons/credit-cards/png/credit-card.png'
        else:
            path = 'icons/credit-cards/png/%s.png' % self.brand
        return static(path)


class Invoice(models.Model):

    STATUSES = (
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('uncollectible', 'Uncollectible'),
        ('void', 'Void')
    )

    stripe_id = models.CharField(
        max_length=150,
        unique=True,
    )
    created = models.DateTimeField()
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        'billing.Subscription',
        on_delete=models.CASCADE
    )
    pdf_url = models.URLField()
    hosted_invoice_url = models.URLField()
    status = models.CharField(
        max_length=25,
        choices=STATUSES
    )
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    amount_due = models.PositiveIntegerField()
    amount_paid = models.PositiveIntegerField()
    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s %s - %s" % (self.company.name, self.period_start, self.period_end)

    @property
    def amount_paid_formatted(self):
        return "$%s" % "{:.2f}".format((self.amount_paid / 100))

    @property
    def paid_at_date_pretty(self):
        if self.paid_at:
            return self.paid_at.strftime("%m/%d")
        else:
            return  None
