# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0008_materials_client_vfd_motor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Labor_Client_VFD_Motor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=160, verbose_name=b'Item')),
                ('vendor', models.CharField(max_length=160, verbose_name=b'Vendor')),
                ('hourly_rate', models.FloatField(default=0, verbose_name=b'Hourly Rate')),
                ('fixed_cost', models.FloatField(default=0, verbose_name=b'Fixed Cost')),
                ('ges_cost', models.FloatField(default=0.0, verbose_name=b'GES Cost')),
                ('ges_markup', models.FloatField(default=0.0, verbose_name=b'GES Markup')),
                ('quantity', models.FloatField(default=0, verbose_name=b'Quantity')),
                ('client_vfd', models.ForeignKey(to='vfd_app.Client_Vfd_Motor')),
            ],
        ),
    ]
