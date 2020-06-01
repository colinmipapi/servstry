# Generated by Django 3.0.6 on 2020-06-01 21:46

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    model_list = ['Coupon', 'Invoice', 'PaymentMethod', 'Plan', 'Subscription']
    for model_name in model_list:
        MyModel = apps.get_model('billing', model_name)
        for row in MyModel.objects.all():
            row.public_id = uuid.uuid4()
            row.save(update_fields=['public_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_add_uuid_field'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
