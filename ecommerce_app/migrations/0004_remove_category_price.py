# Generated by Django 4.1 on 2022-08-19 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerce_app", "0003_category_created_at_category_public_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="price",
        ),
    ]
