# Generated by Django 4.2 on 2024-05-26 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userpayment_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='screenshot',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
