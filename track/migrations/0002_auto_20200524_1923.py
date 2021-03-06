# Generated by Django 3.0.6 on 2020-05-24 19:23

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestvisit',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail Address'),
        ),
        migrations.AlterField(
            model_name='guestvisit',
            name='first_name',
            field=models.CharField(max_length=300, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='guestvisit',
            name='last_name',
            field=models.CharField(max_length=300, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='guestvisit',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='US', verbose_name='Phone Number'),
        ),
    ]
