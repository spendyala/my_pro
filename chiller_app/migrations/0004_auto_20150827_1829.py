# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chiller_app', '0003_auto_20150827_1741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='condensate_pump',
            old_name='condensate_loop_pump_name',
            new_name='condensate_pump_name',
        ),
        migrations.AddField(
            model_name='chiller_images',
            name='chiller_images_name',
            field=models.CharField(default=b'', max_length=256, verbose_name=b'Image Name'),
        ),
    ]
