# Generated by Django 3.0.6 on 2020-05-31 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('companies', '0007_auto_20200528_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='default_payment_method',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_default', to='billing.PaymentMethod'),
        ),
    ]
