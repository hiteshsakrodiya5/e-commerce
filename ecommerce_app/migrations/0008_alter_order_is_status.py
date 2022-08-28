# Generated by Django 4.1 on 2022-08-28 15:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0007_alter_order_cancel_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_status',
            field=models.CharField(blank=True, choices=[('active', 'active'), ('inactive', 'inactive')], default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
    ]
