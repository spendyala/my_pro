# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0003_auto_20150808_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client_vfd',
            old_name='existing_morot_efficiency',
            new_name='existing_motor_efficiency',
        ),
    ]
