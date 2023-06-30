# Generated by Django 3.0 on 2023-06-29 19:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20230629_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='id_number',
            field=models.CharField(default=1, max_length=15, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 13, 19, 16, 26, 760840, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='studentbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 13, 19, 16, 26, 760840, tzinfo=utc), null=True),
        ),
    ]