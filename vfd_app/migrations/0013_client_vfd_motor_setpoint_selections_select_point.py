# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0012_auto_20150904_0338'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_vfd_motor_setpoint_selections',
            name='select_point',
            field=models.IntegerField(default=1, verbose_name=b'Setpoint id'),
        ),
    ]
