# Generated by Django 3.2.11 on 2023-02-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doxer', '0004_auto_20221208_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='firebase_notifications',
            name='cancel_by',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
