# Generated by Django 4.0.4 on 2022-05-26 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='margin_price',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='price',
        ),
    ]
