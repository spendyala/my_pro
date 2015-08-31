from django.db import models
from django.utils import timezone
import datetime
from main_app.models import Client

COMPRESSOR_TYPE = [('REC', 'Reciprocating'),
				   ('ROS', 'Rotary Screw'),
				   ('ROC', 'Rotary Centrifugal')]

CHILLER_TYPE = [('CC', 'Compression Chiller'),
				('ELC', 'Electric Chillers'),
				('VC', 'Vapour Chiller '),
				('AC', 'Absorbtion Chillers'),
				('EVC', 'Evaporative Chillers')]


class Chiller(models.Model):
	client = models.ForeignKey(Client)
	project_name = models.CharField('Project Name', max_length=128)
	electric_utility_rate = models.FloatField('Electric Utility Rate', default=0)

	chiller_name = models.CharField('Chiller Name', max_length=256)
	chiller_model_number = models.CharField('Chiller Model #', max_length=256)
	chiller_manufacturer = models.CharField('Chiller Manufacturer', max_length=256)
	chiller_serial_number = models.CharField('Chiller Serial Number', max_length=256)
	chiller_type = models.CharField('Chiller Type',
									choices=CHILLER_TYPE,
									max_length=256,
									default='EVC')
	compressor_type = models.CharField('Compressor Type',
									   choices=COMPRESSOR_TYPE,
									   max_length=256,
									   default='REC')
	nameplate_capacity = models.FloatField('Nameplate Capacity', default=0)
	rated_kw = models.FloatField('Rated KW', default=0)
	nameplate_max_flow = models.FloatField('Nameplate Max Flow', default=0)
	input_design_water_temp = models.FloatField('Input Design Water Temp', default=0)
	output_design_water_temp = models.FloatField('Output Design Water Temp', default=0)
	rated_flow = models.FloatField('Rated Flow', default=0)
	rated_temp_drop = models.FloatField('Rated Temp Drop', default=0)
	typical_percent_loaded = models.FloatField('Typical Percent Loaded', default=0)
	annual_hours_of_operation = models.FloatField('Annual Hours of Operation', default=0)

	cooling_tower_inlet_temp_in_out_pipe = models.FloatField('Cooling Tower Inlet Temp Measured At In & Out Pipe Fittings', default=0)
	cooling_tower_outlet_temp_in_out_pipe = models.FloatField('Cooling Tower Outlet Temp Measured At In & Out Pipe Fittings', default=0)
	cooling_tower_inlet_temp_oper_display_screen = models.FloatField('Cooling Tower Inlet Temp From Operator Display Screen', default=0)
	cooling_tower_outlet_temp_oper_display_screen = models.FloatField('Cooling Tower Outlet Temp From Operator Display Screen', default=0)

	chilled_water_inlet_temp_in_out_pipe = models.FloatField('Chilled Water Inlet Temp Measured At In & Out Pipe Fittings', default=0)
	chilled_water_outlet_temp_in_out_pipe = models.FloatField('Chilled Water Outlet Temp Measured At In & Out Pipe Fittings', default=0)
	chilled_water_inlet_temp_oper_display_screen = models.FloatField('Chilled Water Inlet Temp From Operator Display Screen', default=0)
	chilled_water_outlet_temp_oper_display_screen = models.FloatField('Chilled Water Outlet Temp From Operator Display Screen', default=0)

	def get_chiller_information_tons_kw(self):
		try:
			return float(round(self.nameplate_capacity/self.rated_kw, 2))
		except Exception as error:
			return 0

	def get_chiller_information_m3_hour(self):
		try:
			return float(round(self.rated_flow/4.4028, 2))
		except Exception as error:
			return 0

	# def get_chill_pump_information_totals(self):
	# 	if self.chill_loop_pump_1:
	# 		return self.chill_loop_pump_1 + self.condensate_pump_1
	# 	else:
	# 		return self.chill_loop_pump_2 + self.condensate_pump_2
	#
	# def get_chill_loop_info_kwh(self, pump_val, annual_flag=False):
	# 	# if self.chill_loop_pump_1:
	# 	# 	chill_loop_pump = self.chill_loop_pump_1
	# 	# 	condensate_pump = self.condensate_pump_1
	# 	# else:
	# 	# 	chill_loop_pump = self.chill_loop_pump_2
	# 	# 	condensate_pump = self.condensate_pump_2
	# 	val = pump_val * 0.746 * 0.9 * self.annual_hours_of_operation
	# 	if annual_flag:
	# 		return round(val)
	# 	return round(val/365.0)
	#
	# def get_chill_loop_info_kwh_totals(self, annual_flag=False):
	# 	if self.chill_loop_pump_1:
	# 		return (self.get_chill_loop_info_daily_kwh(self.chill_loop_pump_1, annual_flag) +
	# 			self.get_chill_loop_info_daily_kwh(self.condensate_pump_1, annual_flag))
	# 	else:
	# 		return (self.get_chill_loop_info_daily_kwh(self.chill_loop_pump_2, annual_flag) +
	# 			self.get_chill_loop_info_daily_kwh(self.condensate_pump_2, annual_flag))
	#
	# def get_chill_loop_info_cost(self, pump_val, annual_flag=False):
	# 	return self.electric_utility_rate * self.get_chill_loop_info_daily_kwh(pump_val, annual_flag)
	#
	# def get_chill_loop_info_cost_total(self, annual_flag=False):
	# 	if self.chill_loop_pump_1:
	# 		return (self.get_chill_loop_info_daily_cost(self.chill_loop_pump_1, annual_flag) +
	# 			self.get_chill_loop_info_daily_cost(self.condensate_pump_1, annual_flag))
	# 	else:
	# 		return (self.get_chill_loop_info_daily_cost(self.chill_loop_pump_2, annual_flag) +
	# 			self.get_chill_loop_info_daily_cost(self.condensate_pump_2, annual_flag))

	def get_cooling_tower_temperature_in_and_out_pipe(self):
		return self.cooling_tower_inlet_temp_in_out_pipe - self.cooling_tower_outlet_temp_in_out_pipe

	def get_cooling_tower_temperature_oper_display_screen(self):
		return self.cooling_tower_inlet_temp_oper_display_screen - self.cooling_tower_outlet_temp_oper_display_screen

	def get_chiller_loop_temp_in_out_pipe(self):
		return self.chilled_water_inlet_temp_in_out_pipe - self.chilled_water_outlet_temp_in_out_pipe

	def get_chiller_loop_temp_oper_display_screen(self):
		return self.chilled_water_inlet_temp_oper_display_screen - self.chilled_water_outlet_temp_oper_display_screen

	def get_chiller_loop_temp_measured_capacity_percent(self):
		return self.get_chiller_loop_temp_in_out_pipe() * self.rated_temp_drop

	def get_chiller_loop_temp_oper_display_screen_percent(self):
		return self.get_chiller_loop_temp_oper_display_screen() * self.rated_temp_drop

	def get_measured_tons_of_cooling(self):
		return self.nameplate_capacity * self.get_chiller_loop_temp_measured_capacity_percent() / 100.0

	def get_display_tons_of_cooling(self):
		return self.nameplate_capacity * self.get_chiller_loop_temp_oper_display_screen() / 10.0

	def get_gal_per_min_confirmation_of_chiller_rated_temp_drop(self):
		return self.rated_flow

	def get_nameplate_tons_confirmation_of_chiller_rated_temp_drop(self):
		return self.nameplate_capacity

	def get_lbs_per_min_confirmation_of_chiller_rated_temp_drop(self):
		return self.rated_flow * 8.34

	def get_btu_per_min_confirmation_of_chiller_rated_temp_drop(self):
		return self.nameplate_capacity * 200.0

	def get_calculated_temp_drop(self):
		try:
			return round(self.get_btu_per_min_confirmation_of_chiller_rated_temp_drop()/
				self.get_lbs_per_min_confirmation_of_chiller_rated_temp_drop(), 2)
		except Exception as error:
			return 0

	def get_compare_to_nameplate_rated_temp_drop(self):
		return self.rated_temp_drop

	def annual_cost_of_operation_kw_during_typical_operation(self):
		return (self.rated_kw * self.typical_percent_loaded )/ 100.0

	def get_cost_of_chiller_operation_only_annualy(self):
		return (self.annual_cost_of_operation_kw_during_typical_operation() *
			self.annual_hours_of_operation)

	def get_cost_of_chiller_operation_only_daily(self):
		return (self.annual_cost_of_operation_kw_during_typical_operation() *
			(self.annual_hours_of_operation/365.0))

	def get_cost_of_chiller_operation_only_annual_cost(self):
		return self.get_cost_of_chiller_operation_only_annualy() * self.electric_utility_rate

	def __str__(self):
		return self.chiller_name


class Chiller_Loop_Pump(models.Model):
	chiller = models.ForeignKey(Chiller)
	chiller_loop_pump_name = models.CharField('Chiller Loop Pump Name', max_length=256, default='')
	chill_loop_pump = models.FloatField('Chill Loop Pump', default=0)
	selected = models.BooleanField('Selected', default=False)

	def get_chill_loop_info_kwh(self, annual_flag=False):
		val = self.chill_loop_pump * 0.746 * 0.9 * self.chiller.annual_hours_of_operation
		if annual_flag:
			return round(val)
		return round(val/365.0)

	def __str__(self):
		return self.chiller_loop_pump_name

	def get_chill_loop_info_cost(self, annual_flag=False):
		return self.chiller.electric_utility_rate * self.get_chill_loop_info_kwh(annual_flag)


class Condensate_Pump(models.Model):
	chiller = models.ForeignKey(Chiller)
	condensate_pump_name = models.CharField('Condensate Pump Name', max_length=256, default='')
	condensate_pump = models.FloatField('Condensate Pump', default=0)
	selected = models.BooleanField('Selected', default=False)

	def __str__(self):
		return self.condensate_pump_name

	def get_condensate_info_kwh(self, annual_flag=False):
		val = self.condensate_pump * 0.746 * 0.9 * self.chiller.annual_hours_of_operation
		if annual_flag:
			return round(val)
		return round(val/365.0)

	def get_condensate_info_cost(self, annual_flag=False):
		return self.chiller.electric_utility_rate * self.get_condensate_info_kwh(annual_flag)


class Chiller_Images(models.Model):
	chiller = models.ForeignKey(Chiller)
	chiller_images_name = models.CharField('Image Name', max_length=256, default='')
	image_description = models.TextField('Image Description', max_length=400, default='')
	# make_path = 'chiller_%s' % (chiller.id)
	path_to_image = models.FileField(upload_to='static/images/chiller/%Y/%m/%d')
	# path_to_image = models.FileField(upload_to='images/%Y/%m/%d')

	def __str__(self):
		return self.chiller_images_name
