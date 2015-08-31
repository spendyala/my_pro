# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vfd_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_vfd',
            name='installed_date',
            field=models.DateTimeField(null=True, verbose_name=b'Installed Date'),
        ),
    ]
