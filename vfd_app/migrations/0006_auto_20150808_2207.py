# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20150808_2102'),
        ('vfd_app', '0005_client_vfd_permonth'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Vfd_Motor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vfd_name', models.CharField(max_length=256, verbose_name=b'Client VFD Name')),
                ('cost_per_kwh', models.FloatField(default=0.0, verbose_name=b'Cost per kWh')),
                ('installed_date', models.DateTimeField(null=True, verbose_name=b'Installed Date')),
                ('motor_horse_pwr', models.FloatField(default=0.0, verbose_name=b'Motor Hp')),
                ('existing_motor_efficiency', models.FloatField(default=0, verbose_name=b'Existing Motor Eff.')),
                ('proposed_vfd_efficiency', models.FloatField(default=0.0, verbose_name=b'Proposed VFD Eff.')),
                ('motor_load', models.FloatField(default=0, verbose_name=b'Motor Load')),
                ('client', models.ForeignKey(to='main_app.Client')),
                ('vfd', models.ForeignKey(to='main_app.Vfd')),
            ],
        ),
        migrations.CreateModel(
            name='Client_Vfd_Motor_Data_Per_Month',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.CharField(max_length=3, verbose_name=b'Month', choices=[(b'JAN', b'January'), (b'FEB', b'February'), (b'MAR', b'March'), (b'APR', b'April'), (b'MAY', b'May'), (b'JUN', b'June'), (b'JUL', b'July'), (b'AUG', b'August'), (b'SEP', b'September'), (b'OCT', b'October'), (b'NOV', b'November'), (b'DEC', b'December')])),
                ('hours_of_operation', models.FloatField(default=0, verbose_name=b'Hours of operation')),
                ('client_vfd', models.ForeignKey(to='vfd_app.Client_Vfd_Motor')),
            ],
        ),
        migrations.RemoveField(
            model_name='client_vfd',
            name='client',
        ),
        migrations.RemoveField(
            model_name='client_vfd',
            name='vfd',
        ),
        migrations.RemoveField(
            model_name='client_vfd_permonth',
            name='client_vfd',
        ),
        migrations.DeleteModel(
            name='Client_Vfd',
        ),
        migrations.DeleteModel(
            name='Client_Vfd_permonth',
        ),
    ]
