# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0010_labor_client_vfd_motor_fixed_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_vfd_motor_data_per_month',
            name='percent_of_time',
            field=models.FloatField(default=0, verbose_name=b'Percent of time'),
        ),
    ]
