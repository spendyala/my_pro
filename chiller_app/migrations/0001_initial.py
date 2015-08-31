# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_client_customer_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chiller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=128, verbose_name=b'Project Name')),
                ('electric_utility_rate', models.FloatField(default=0, verbose_name=b'Electric Utility Rate')),
                ('chiller_name', models.CharField(max_length=256, verbose_name=b'Chiller Name')),
                ('chiller_model_number', models.CharField(max_length=256, verbose_name=b'Chiller Model #')),
                ('chiller_type', models.CharField(max_length=256, verbose_name=b'Chiller Type')),
                ('chiller_manufacturer', models.CharField(max_length=256, verbose_name=b'Chiller Manufacturer')),
                ('chiller_serial_number', models.CharField(max_length=256, verbose_name=b'Chiller Serial Number')),
                ('compressor_type', models.CharField(max_length=256, verbose_name=b'Compressor Type')),
                ('nameplate_capacity', models.FloatField(default=0, verbose_name=b'Nameplate Capacity')),
                ('rated_kw', models.FloatField(default=0, verbose_name=b'Rated KW')),
                ('nameplate_max_flow', models.FloatField(default=0, verbose_name=b'Nameplate Max Flow')),
                ('input_design_water_temp', models.FloatField(default=0, verbose_name=b'Input Design Water Temp')),
                ('output_design_water_temp', models.FloatField(default=0, verbose_name=b'Output Design Water Temp')),
                ('rated_flow', models.FloatField(default=0, verbose_name=b'Rated Flow')),
                ('rated_temp_drop', models.FloatField(default=0, verbose_name=b'Rated Temp Drop')),
                ('typical_percent_loaded', models.FloatField(default=0, verbose_name=b'Typical Percent Loaded')),
                ('annual_hours_of_operation', models.FloatField(default=0, verbose_name=b'Annual Hours of Operation')),
                ('cooling_tower_inlet_temp_in_out_pipe', models.FloatField(default=0, verbose_name=b'Cooling Tower Inlet Temp Measured At In & Out Pipe Fittings')),
                ('cooling_tower_outlet_temp_in_out_pipe', models.FloatField(default=0, verbose_name=b'Cooling Tower Outlet Temp Measured At In & Out Pipe Fittings')),
                ('cooling_tower_inlet_temp_oper_display_screen', models.FloatField(default=0, verbose_name=b'Cooling Tower Inlet Temp From Operator Display Screen')),
                ('cooling_tower_outlet_temp_oper_display_screen', models.FloatField(default=0, verbose_name=b'Cooling Tower Outlet Temp From Operator Display Screen')),
                ('chilled_water_inlet_temp_in_out_pipe', models.FloatField(default=0, verbose_name=b'Chilled Water Inlet Temp Measured At In & Out Pipe Fittings')),
                ('chilled_water_outlet_temp_in_out_pipe', models.FloatField(default=0, verbose_name=b'Chilled Water Outlet Temp Measured At In & Out Pipe Fittings')),
                ('chilled_water_inlet_temp_oper_display_screen', models.FloatField(default=0, verbose_name=b'Chilled Water Inlet Temp From Operator Display Screen')),
                ('chilled_water_outlet_temp_oper_display_screen', models.FloatField(default=0, verbose_name=b'Chilled Water Outlet Temp From Operator Display Screen')),
                ('client', models.ForeignKey(to='main_app.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Chiller_Loop_Pump',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chill_loop_pump', models.FloatField(default=0, verbose_name=b'Chill Loop Pump')),
                ('chiller', models.ForeignKey(to='chiller_app.Chiller')),
            ],
        ),
        migrations.CreateModel(
            name='Condensate_Pump',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condensate_pump', models.FloatField(default=0, verbose_name=b'Condensate Pump')),
                ('chiller', models.ForeignKey(to='chiller_app.Chiller')),
            ],
        ),
    ]
