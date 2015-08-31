# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chiller_app', '0005_auto_20150827_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='chiller_images',
            name='image_description',
            field=models.TextField(default=b'', max_length=400, verbose_name=b'Image Description'),
        ),
        migrations.AlterField(
            model_name='chiller_images',
            name='path_to_image',
            field=models.FileField(upload_to=b'static/images/chiller/%Y/%m/%d'),
        ),
    ]
