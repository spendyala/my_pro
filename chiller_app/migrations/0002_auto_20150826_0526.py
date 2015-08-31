# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chiller_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chiller_Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_to_image', models.CharField(default=b'', max_length=500, verbose_name=b'Images Path')),
            ],
        ),
        migrations.AlterField(
            model_name='chiller',
            name='chiller_type',
            field=models.CharField(default=b'EVC', max_length=256, verbose_name=b'Chiller Type', choices=[(b'CC', b'Compression Chiller'), (b'ELC', b'Electric Chillers'), (b'VC', b'Vapour Chiller '), (b'AC', b'Absorbtion Chillers'), (b'EVC', b'Evaporative Chillers')]),
        ),
        migrations.AlterField(
            model_name='chiller',
            name='compressor_type',
            field=models.CharField(default=b'REC', max_length=256, verbose_name=b'Compressor Type', choices=[(b'REC', b'Reciprocating'), (b'ROS', b'Rotary Screw'), (b'ROC', b'Rotary Centrifugal')]),
        ),
        migrations.AddField(
            model_name='chiller_images',
            name='chiller',
            field=models.ForeignKey(to='chiller_app.Chiller'),
        ),
    ]
