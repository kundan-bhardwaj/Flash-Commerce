# Generated by Django 4.2.16 on 2024-10-20 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_product_created_at_alter_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
