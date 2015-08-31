# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0004_auto_20150808_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Vfd_permonth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.CharField(max_length=3, verbose_name=b'Month', choices=[(b'JAN', b'January'), (b'FEB', b'February'), (b'MAR', b'March'), (b'APR', b'April'), (b'MAY', b'May'), (b'JUN', b'June'), (b'JUL', b'July'), (b'AUG', b'August'), (b'SEP', b'September'), (b'OCT', b'October'), (b'NOV', b'November'), (b'DEC', b'December')])),
                ('hours_of_operation', models.FloatField(default=0, verbose_name=b'Hours of operation')),
                ('client_vfd', models.ForeignKey(to='vfd_app.Client_Vfd')),
            ],
        ),
    ]
