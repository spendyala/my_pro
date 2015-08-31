# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chiller_app', '0002_auto_20150826_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='chiller_loop_pump',
            name='chiller_loop_pump_name',
            field=models.CharField(default=b'', max_length=256, verbose_name=b'Chiller Loop Pump Name'),
        ),
        migrations.AddField(
            model_name='condensate_pump',
            name='condensate_loop_pump_name',
            field=models.CharField(default=b'', max_length=256, verbose_name=b'Condensate Pump Name'),
        ),
    ]
