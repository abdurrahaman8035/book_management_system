# Generated by Django 3.0 on 2023-06-25 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20230625_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 16, 17, 40, 1, 283173), null=True),
        ),
        migrations.AlterField(
            model_name='staffbook',
            name='issued_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 25, 17, 40, 1, 283105)),
        ),
        migrations.AlterField(
            model_name='studentbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 9, 17, 40, 1, 282219), null=True),
        ),
        migrations.AlterField(
            model_name='studentbook',
            name='issued_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 25, 17, 40, 1, 282143)),
        ),
    ]