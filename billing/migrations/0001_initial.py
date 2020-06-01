# Generated by Django 3.0.6 on 2020-05-31 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0007_auto_20200528_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=300)),
                ('created', models.DateTimeField()),
                ('discount', models.PositiveIntegerField()),
                ('duration', models.CharField(choices=[('once', 'Once'), ('recurring', 'Recurring'), ('forever', 'Forever')], max_length=25)),
                ('duration_in_months', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=150)),
                ('created', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('price', models.PositiveIntegerField()),
                ('interval', models.CharField(choices=[('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=150)),
                ('created', models.DateTimeField()),
                ('status', models.CharField(choices=[('incomplete', 'Incomplete'), ('incomplete_expired', 'Incomplete Expired'), ('trialing', 'Trailing'), ('active', 'Active'), ('past_due', 'Past Due'), ('canceled', 'Canceled'), ('unpaid', 'Unpaid')], max_length=25)),
                ('next_pending_invoice', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='billing.Coupon')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.Plan')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=150)),
                ('created', models.DateTimeField()),
                ('brand', models.CharField(choices=[('amex', 'American Express'), ('diners', 'Diners Club'), ('discover', 'Discover'), ('jcb', 'JCB'), ('mastercard', 'MasterCard'), ('unionpay', 'UnionPay'), ('visa', 'Visa'), ('unknown', 'Unknown')], max_length=25)),
                ('last4', models.CharField(max_length=4)),
                ('exp_month', models.CharField(max_length=2)),
                ('exp_year', models.CharField(max_length=4)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='companies.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=150)),
                ('created', models.DateTimeField()),
                ('pdf_url', models.URLField()),
                ('hosted_invoice_url', models.URLField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid'), ('uncollectible', 'Uncollectible'), ('void', 'Void')], max_length=25)),
                ('period_start', models.DateTimeField()),
                ('period_end', models.DateTimeField()),
                ('amount_due', models.PositiveIntegerField()),
                ('amount_paid', models.PositiveIntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.Subscription')),
            ],
        ),
    ]
