# Generated by Django 4.0.4 on 2022-06-08 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_variation_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='varientsize',
            name='product',
        ),
        migrations.AddField(
            model_name='varientsize',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
