# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chiller_app', '0004_auto_20150827_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='chiller_loop_pump',
            name='selected',
            field=models.BooleanField(default=False, verbose_name=b'Selected'),
        ),
        migrations.AddField(
            model_name='condensate_pump',
            name='selected',
            field=models.BooleanField(default=False, verbose_name=b'Selected'),
        ),
    ]
