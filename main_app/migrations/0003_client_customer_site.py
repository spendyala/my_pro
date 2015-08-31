# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20150808_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='customer_site',
            field=models.CharField(default=b'', max_length=256, verbose_name=b'Customer Site'),
        ),
    ]
