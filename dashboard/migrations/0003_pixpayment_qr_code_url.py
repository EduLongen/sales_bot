# Generated by Django 5.1.2 on 2024-11-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_pixpayment_qr_code_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pixpayment',
            name='qr_code_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
