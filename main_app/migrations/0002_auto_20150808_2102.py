# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vfd',
            name='cost_per_kwh',
        ),
        migrations.AlterField(
            model_name='vfd',
            name='vfd_install_date',
            field=models.DateTimeField(null=True, verbose_name=b'Added Date'),
        ),
    ]
