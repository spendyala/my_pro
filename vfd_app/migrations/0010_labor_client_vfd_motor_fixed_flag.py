# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0009_labor_client_vfd_motor'),
    ]

    operations = [
        migrations.AddField(
            model_name='labor_client_vfd_motor',
            name='fixed_flag',
            field=models.BooleanField(default=True, verbose_name=b'Fixed Labor Flag'),
        ),
    ]
