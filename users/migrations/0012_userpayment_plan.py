# Generated by Django 4.2 on 2024-05-28 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_current_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.plan'),
        ),
    ]
