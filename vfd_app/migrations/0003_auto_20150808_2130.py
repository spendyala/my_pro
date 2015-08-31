# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0002_client_vfd_installed_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_vfd',
            name='existing_morot_efficiency',
            field=models.FloatField(default=0, verbose_name=b'Existing Motor Eff.'),
        ),
        migrations.AddField(
            model_name='client_vfd',
            name='motor_horse_pwr',
            field=models.FloatField(default=0.0, verbose_name=b'Motor Hp'),
        ),
        migrations.AddField(
            model_name='client_vfd',
            name='motor_load',
            field=models.FloatField(default=0, verbose_name=b'Motor Load'),
        ),
        migrations.AddField(
            model_name='client_vfd',
            name='proposed_vfd_efficiency',
            field=models.FloatField(default=0.0, verbose_name=b'Proposed VFD Eff.'),
        ),
        migrations.AlterField(
            model_name='client_vfd',
            name='vfd_name',
            field=models.CharField(max_length=256, verbose_name=b'Client VFD Name'),
        ),
    ]
