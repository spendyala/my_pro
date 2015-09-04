# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0011_client_vfd_motor_data_per_month_percent_of_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Vfd_Motor_Setpoint_Selections',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('speed_percent', models.FloatField(default=0, verbose_name=b'VFD Speed %')),
                ('percent_of_time', models.FloatField(default=0, verbose_name=b'Percent Of Time (%)')),
                ('client_vfd', models.ForeignKey(to='vfd_app.Client_Vfd_Motor')),
            ],
        ),
        migrations.RemoveField(
            model_name='client_vfd_motor_data_per_month',
            name='percent_of_time',
        ),
        migrations.RemoveField(
            model_name='client_vfd_motor_data_per_month',
            name='vfd_set_point',
        ),
    ]
