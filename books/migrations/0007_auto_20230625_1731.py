# Generated by Django 3.0 on 2023-06-25 16:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20230625_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Book title')),
                ('issued_date', models.DateTimeField(default=datetime.datetime(2023, 6, 25, 17, 31, 47, 218469))),
                ('added_days', models.IntegerField(blank=True, null=True)),
                ('remaining_days', models.CharField(blank=True, max_length=100, null=True)),
                ('expiring_date', models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 9, 17, 31, 47, 218577), null=True)),
                ('borrowed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.Student')),
            ],
            options={
                'ordering': ['-issued_date'],
            },
        ),
        migrations.AlterField(
            model_name='staffbook',
            name='expiring_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 9, 17, 31, 47, 218577), null=True),
        ),
        migrations.AlterField(
            model_name='staffbook',
            name='issued_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 25, 17, 31, 47, 218469)),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
