# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20150808_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Vfd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vfd_name', models.CharField(max_length=256, verbose_name=b'Client')),
                ('cost_per_kwh', models.FloatField(default=0.0, verbose_name=b'Cost per kWh')),
                ('client', models.ForeignKey(to='main_app.Client')),
                ('vfd', models.ForeignKey(to='main_app.Vfd')),
            ],
        ),
    ]
