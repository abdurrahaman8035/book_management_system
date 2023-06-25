# Generated by Django 3.0 on 2023-06-25 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20230625_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 9, 17, 25, 28, 949008), null=True),
        ),
        migrations.AlterField(
            model_name='staffbook',
            name='issued_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 25, 17, 25, 28, 948908)),
        ),
        migrations.AlterField(
            model_name='studentbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 9, 17, 25, 28, 949008), null=True),
        ),
        migrations.AlterField(
            model_name='studentbook',
            name='issued_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 25, 17, 25, 28, 948908)),
        ),
    ]