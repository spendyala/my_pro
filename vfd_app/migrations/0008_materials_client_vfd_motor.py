# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0007_client_vfd_motor_data_per_month_vfd_set_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materials_Client_VFD_Motor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=160, verbose_name=b'Item')),
                ('supplier', models.CharField(max_length=160, verbose_name=b'Supplier')),
                ('description', models.CharField(max_length=500, verbose_name=b'Description')),
                ('ges_cost_each', models.FloatField(default=0.0, verbose_name=b'GES Cost Each')),
                ('ges_markup', models.FloatField(default=0.0, verbose_name=b'GES Markup')),
                ('quantity', models.FloatField(default=0, verbose_name=b'Quantity')),
                ('client_vfd', models.ForeignKey(to='vfd_app.Client_Vfd_Motor')),
            ],
        ),
    ]
