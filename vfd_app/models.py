from django.db import models
from django.utils import timezone
import datetime
from main_app.models import Client, Vfd

MONTHS = [('JAN', 'January'),
		  ('FEB', 'February'),
		  ('MAR', 'March'),
		  ('APR', 'April'),
		  ('MAY', 'May'),
		  ('JUN', 'June'),
		  ('JUL', 'July'),
		  ('AUG', 'August'),
		  ('SEP', 'September'),
		  ('OCT', 'October'),
		  ('NOV', 'November'),
		  ('DEC', 'December')]


class Client_Vfd_Motor(models.Model):
	client = models.ForeignKey(Client)
	vfd = models.ForeignKey(Vfd)
	vfd_name = models.CharField('Client VFD Name', max_length=256)
	cost_per_kwh = models.FloatField('Cost per kWh', default=0.00)
	installed_date = models.DateTimeField('Installed Date', null=True)
	motor_horse_pwr = models.FloatField('Motor Hp', default=0.00)
	existing_motor_efficiency = models.FloatField('Existing Motor Eff.',
												  default=0)
	proposed_vfd_efficiency = models.FloatField('Proposed VFD Eff.',
												default=0.0)
	motor_load = models.FloatField('Motor Load', default=0)

	def was_recent(self):
		if not self.installed_date:
			return False
		return (self.installed_date >=
				timezone.now() - datetime.timedelta(days=1))
	was_recent.admin_order_field = 'installed_date'
	was_recent.boolean = True
	was_recent.short_description = 'Recently installed?'

	def __str__(self):
		return self.vfd_name


class Client_Vfd_Motor_Data_Per_Month(models.Model):
	client_vfd = models.ForeignKey(Client_Vfd_Motor)
	month = models.CharField('Month',
							 max_length=3,
							 choices=MONTHS)
	hours_of_operation = models.FloatField('Hours of operation',
										   default=0)

	def __str__(self):
		return '%s-%s' % (self.client_vfd, self.month)


class Client_Vfd_Motor_Setpoint_Selections(models.Model):
	client_vfd = models.ForeignKey(Client_Vfd_Motor)
	speed_percent = models.FloatField('VFD Speed %', default=0)
	percent_of_time = models.FloatField('Percent Of Time (%)', default=0)
	select_point = models.IntegerField('Setpoint id', default=1)


class Materials_Client_VFD_Motor(models.Model):
	client_vfd = models.ForeignKey(Client_Vfd_Motor)
	item = models.CharField('Item', max_length=160)
	supplier = models.CharField('Supplier', max_length=160)
	description = models.CharField('Description', max_length=500)
	ges_cost_each = models.FloatField('GES Cost Each', default=0.0)
	ges_markup = models.FloatField('GES Markup', default=0.0)
	quantity = models.FloatField('Quantity', default=0)


class Labor_Client_VFD_Motor(models.Model):
	client_vfd = models.ForeignKey(Client_Vfd_Motor)
	item = models.CharField('Item', max_length=160)
	vendor = models.CharField('Vendor', max_length=160)
	hourly_rate = models.FloatField('Hourly Rate', default=0)
	fixed_cost = models.FloatField('Fixed Cost', default=0)
	ges_cost = models.FloatField('GES Cost', default=0.0)
	ges_markup = models.FloatField('GES Markup', default=0.0)
	quantity = models.FloatField('Quantity', default=0)
	fixed_flag = models.BooleanField('Fixed Labor Flag', default=True)
