# Generated by Django 4.2.6 on 2023-11-29 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]