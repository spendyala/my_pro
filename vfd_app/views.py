from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from .models import (Client_Vfd_Motor,
					 Client_Vfd_Motor_Data_Per_Month,
					 Materials_Client_VFD_Motor,
					 Labor_Client_VFD_Motor,
					 Client_Vfd_Motor_Setpoint_Selections)
from main_app.models import Client, Vfd
from django.core.urlresolvers import reverse

import datetime

import json


MONTHS_ORDER = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
				'OCT', 'NOV', 'DEC']
MAX_HOURS_PER_MONTH = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

# VFD_SET_POINTS = [100, 90, 80, 70, 60, 50, 40, 30]
VFD_SET_POINTS = [100]


def index(request):
	try:
		client_vfd_motor_objs = Client_Vfd_Motor.objects.order_by('-vfd_name')
	except Exception as exception:
		return Http404('Page not found')
	context = {'client_vfd_motor_objs': client_vfd_motor_objs}
	return render(request, 'vfd_app/index.html', context)


def detail(request, client_vfd_id, vfd_set_point):
	context = {'client_vfd_view': get_client_vfd_view_obj(client_vfd_id,
														  vfd_set_point)}
	return render(request, 'vfd_app/detail.html', context)


def search_form(request):
	context = {'data': 'data'}
	return render(request, 'vfd_app/search_form.html', context)


def save_new_vfd(request):
	client_vfd_obj = Client_Vfd_Motor()
	client_vfd_obj.installed_date = datetime.datetime.now()
	new_client_obj = Client.objects.get(id=request.POST['new_client_obj'])
	new_vfd_obj = Vfd.objects.get(id=request.POST['new_vfd_obj'])
	client_vfd_obj.client = new_client_obj
	client_vfd_obj.vfd = new_vfd_obj
	client_vfd_obj.vfd_name = request.POST['vfd_name']
	client_vfd_obj.cost_per_kwh = float(request.POST['cost_per_kwh'])
	client_vfd_obj.motor_horse_pwr = float(request.POST['motor_horse_pwr'])
	client_vfd_obj.existing_motor_efficiency = float(request.POST[
		'existing_motor_efficiency'])
	client_vfd_obj.proposed_vfd_efficiency = float(request.POST[
		'proposed_vfd_efficiency'])
	client_vfd_obj.motor_load = float(request.POST['motor_load'])
	client_vfd_obj.save()
	return client_vfd_obj.id


def save_data(request, client_vfd_id):
	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	client_vfd_obj.vfd_name = request.POST['vfd_name']
	client_vfd_obj.cost_per_kwh = float(request.POST['cost_per_kwh'])
	client_vfd_obj.motor_horse_pwr = float(request.POST['motor_horse_pwr'])
	client_vfd_obj.existing_motor_efficiency = float(request.POST[
		'existing_motor_efficiency'])
	client_vfd_obj.proposed_vfd_efficiency = float(request.POST[
		'proposed_vfd_efficiency'])
	client_vfd_obj.motor_load = float(request.POST['motor_load'])
	client_vfd_obj.save()


def save_monthly_hour(request, client_vfd_id):
	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	for each_month in MONTHS_ORDER:
		monthly_val = request.POST['proposed_%s' % (each_month.lower(),)].strip()
		print 'here', monthly_val
		if not monthly_val:
			monthly_val = 0
		else:
			monthly_val = float(monthly_val)
		monthly_obj, create_flag = Client_Vfd_Motor_Data_Per_Month.objects.get_or_create(client_vfd=client_vfd_obj, month=each_month)
		monthly_obj.hours_of_operation = monthly_val
		monthly_obj.save()

def save_setpoints(request, client_vfd_id):
	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	for each_setpoint in [1, 2, 3, 4]:
		set_point_obj, create_flag = Client_Vfd_Motor_Setpoint_Selections.objects.get_or_create(client_vfd=client_vfd_obj,
			select_point=each_setpoint)
		set_point_obj.speed_percent = request.POST['%s_vfd_speed' % (each_setpoint,)].strip() or 0
		set_point_obj.percent_of_time = request.POST['%s_percent_of_time' % (each_setpoint,)].strip() or 0
		set_point_obj.save()


def installation_pricing_materials(client_vfd_id, miss_materials_percent = 10):
	materials_data = {}
	materials_data['list'] = []

	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	materials_list = Materials_Client_VFD_Motor.objects.filter(client_vfd=client_vfd_obj.id)
	total_material_cost = 0
	for each_material in materials_list:
		material_info = {}
		material_info['quantity'] = each_material.quantity
		material_info['item'] = each_material.item
		material_info['supplier'] = each_material.supplier
		material_info['description'] = each_material.description
		material_info['ges_cost_each'] = each_material.ges_cost_each
		material_info['ges_markup'] = each_material.ges_markup
		try:
			material_info['customer_each_price'] = int(round(each_material.ges_cost_each/each_material.ges_markup))
		except Exception:
			material_info['customer_each_price'] = 0
		material_info['extended_cost'] = material_info['customer_each_price'] * each_material.quantity
		materials_data['list'].append(material_info)
		total_material_cost += material_info['extended_cost']
	materials_data['total_material_cost'] = total_material_cost
	materials_data['miss_materials_percent'] = miss_materials_percent
	materials_data['total_material_miss_cost'] = total_material_cost + int(round((total_material_cost * miss_materials_percent)/100.0))
	return materials_data


def installation_pricing_labor(client_vfd_id, miss_labor_percent = 5):
	labor_data = {}
	labor_data['list'] = []

	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	labor_list = Labor_Client_VFD_Motor.objects.filter(client_vfd=client_vfd_obj.id)
	total_labor_cost = 0
	for each_labor in labor_list:
		labor_info = {}
		labor_info['quantity'] = each_labor.quantity
		labor_info['item'] = each_labor.item
		labor_info['vendor'] = each_labor.vendor
		labor_info['hourly_rate'] = each_labor.hourly_rate
		labor_info['fixed_cost'] = each_labor.fixed_cost
		labor_info['ges_cost'] = each_labor.ges_cost
		labor_info['ges_markup'] = each_labor.ges_markup
		try:
			labor_info['customer_price'] = int(round(each_labor.ges_cost/each_labor.ges_markup))
		except Exception as error:
			labor_info['customer_price'] = 0
		labor_data['list'].append(labor_info)
		total_labor_cost += labor_info['customer_price']
	labor_data['total_labor_cost'] = total_labor_cost
	labor_data['miss_labor_percent'] = miss_labor_percent
	try:
		labor_data['total_labor_miss_cost'] = total_labor_cost + int(round((total_labor_cost * miss_labor_percent)/100.0))
	except Exception:
		labor_data['total_labor_miss_cost'] = 0
	return labor_data


def save_material(request, client_vfd_id):
	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	material_obj = Materials_Client_VFD_Motor()
	material_obj.client_vfd = client_vfd_obj
	material_obj.item = request.POST['item']
	material_obj.supplier = request.POST['supplier']
	material_obj.description = request.POST['description']
	material_obj.ges_cost_each = float(request.POST.get('ges_cost_each', 0.00))
	material_obj.ges_markup = float(request.POST.get('ges_markup', 0.0))
	material_obj.quantity = float(request.POST.get('quantity', 0))
	material_obj.save()


def save_labor(request, client_vfd_id):
	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
	labor_obj = Labor_Client_VFD_Motor()
	labor_obj.client_vfd = client_vfd_obj
	labor_obj.item = request.POST['item_labor']
	labor_obj.vendor = request.POST['vendor']
	if not request.POST['hourly_rate']:
		labor_obj.hourly_rate = 0
	else:
		labor_obj.hourly_rate = float(request.POST.get('hourly_rate',0))
	if not request.POST['fixed_cost']:
		labor_obj.fixed_cost = 0
	else:
		labor_obj.fixed_cost = float(request.POST.get('fixed_cost',0))
	labor_obj.ges_cost = float(request.POST.get('ges_cost',0))
	labor_obj.ges_markup = float(request.POST.get('ges_labor_markup', 0.0))
	labor_obj.quantity = float(request.POST.get('quantity_labor', 0))
	labor_obj.save()


def report(request, client_vfd_id):

	data = {}
	data['create_new_vfd'] = False

	if 'create_vfd_flag' in request.POST and request.POST['create_vfd_flag'] == '1':
		vfd_id = save_new_vfd(request)
		redirect_url = '/vfd_app/report/%s/' % (vfd_id,)
		return redirect('/vfd_app/report/%s/' % (vfd_id,))

	if client_vfd_id == 'add':
		data['client_vfd_id'] = 'add'
		data['new_client_objs'] = [(x.id, x.client_name) for x in Client.objects.all()]
		data['new_vfd_objs'] = [(x.id, x.vfd_name) for x in Vfd.objects.all()]
		data['create_new_vfd'] = True
		context = {'data': data}
		return render(request, 'vfd_app/report.html', context)

	if 'save_text' in request.POST and request.POST['save_text'] == '1':
		save_data(request, client_vfd_id)

	if 'save_material' in request.POST and request.POST['save_material'] == '1':
		save_material(request, client_vfd_id)

	if 'save_labor' in request.POST and request.POST['save_labor'] == '1':
		save_labor(request, client_vfd_id)

	if 'save_monthly_hour' in request.POST and request.POST['save_monthly_hour'] == '1':
		save_monthly_hour(request, client_vfd_id)

	if 'save_setpoints' in request.POST and request.POST['save_setpoints'] == '1':
		save_setpoints(request, client_vfd_id)

	total_proposed_vfd_kwh = 0
	total_proposed_cost = 0

	client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)

	vfd_proposed_calculated = round(1/client_vfd_obj.proposed_vfd_efficiency, 2)
	existing_motor_efficiency_calculated = round(1/client_vfd_obj.existing_motor_efficiency, 2)

	data['client_vfd_id'] = client_vfd_obj.id
	data['client_name'] = client_vfd_obj.client.client_name
	data['vfd_actual_name'] = client_vfd_obj.vfd.vfd_name
	data['vfd_name'] = client_vfd_obj.vfd_name
	data['cost_per_kwh'] = client_vfd_obj.cost_per_kwh
	data['installed_date'] = client_vfd_obj.installed_date
	data['motor_horse_pwr'] = client_vfd_obj.motor_horse_pwr
	data['existing_motor_efficiency'] = client_vfd_obj.existing_motor_efficiency
	data['proposed_vfd_efficiency'] = client_vfd_obj.proposed_vfd_efficiency
	data['motor_load'] = client_vfd_obj.motor_load


	data['total_hours'] = 0
	# Montly information
	monthly_hours_operation = Client_Vfd_Motor_Data_Per_Month.objects.filter(client_vfd=client_vfd_obj)
	for each_month_info in monthly_hours_operation:
		data['proposed_%s' % (each_month_info.month.lower())] = each_month_info.hours_of_operation
		data['total_hours'] += each_month_info.hours_of_operation


	try:
		val = float(1.0/client_vfd_obj.existing_motor_efficiency)
		total_kwh = client_vfd_obj.motor_horse_pwr * val
		total_kwh *= client_vfd_obj.motor_load
		total_kwh *= 0.746
		total_kwh *= data['total_hours']
		total_kwh = round(total_kwh, 2)
	except Exception as exception:
		total_kwh = 0

	data['total_existing_kwh'] = total_kwh
	data['total_existing_cost_of_operation'] = round(data['total_existing_kwh'] * client_vfd_obj.cost_per_kwh, 2)

	setpoint_selections = Client_Vfd_Motor_Setpoint_Selections.objects.filter(client_vfd=client_vfd_obj)

	data['total_proposed_cost'] = 0
	data['total_proposed_vfd_kwh'] = 0
	for each_setpoint in setpoint_selections:
		counter = each_setpoint.select_point
		data['%s_vfd_speed' % (counter,)] = each_setpoint.speed_percent
		data['%s_percent_of_time' % (counter,)] = each_setpoint.percent_of_time
		try:
			val_2 = float(1.0/client_vfd_obj.proposed_vfd_efficiency)
			proposed_vfd_kwh = data['total_hours']
			proposed_vfd_kwh *= each_setpoint.percent_of_time
			proposed_vfd_kwh = round(proposed_vfd_kwh/100.0, 2)
			proposed_vfd_kwh *= each_setpoint.speed_percent
			proposed_vfd_kwh = round(proposed_vfd_kwh/100.0, 2)
			proposed_vfd_kwh *= each_setpoint.speed_percent
			proposed_vfd_kwh = round(proposed_vfd_kwh/100.0, 2)
			proposed_vfd_kwh *= each_setpoint.speed_percent
			proposed_vfd_kwh *= client_vfd_obj.motor_horse_pwr
			proposed_vfd_kwh *= val_2 * 0.746
			proposed_vfd_kwh *= client_vfd_obj.motor_load
			proposed_vfd_kwh = round(proposed_vfd_kwh/100.0, 2)
		except Exception as exception:
			proposed_vfd_kwh = 0
		data['%s_proposed_kwh' % (counter,)] = proposed_vfd_kwh
		data['%s_proposed_cost' % (counter,)] = round(proposed_vfd_kwh *
													  client_vfd_obj.cost_per_kwh, 2)
		data['total_proposed_cost'] += data['%s_proposed_cost' % (counter,)]
		data['total_proposed_vfd_kwh'] += data['%s_proposed_kwh' % (counter,)]

	data['annual_kwh_savings'] = data['total_existing_kwh'] - data['total_proposed_vfd_kwh']
	data['annual_cost_savings'] = data['total_existing_cost_of_operation'] - data['total_proposed_cost']

	context = {'data': data}
	return render(request, 'vfd_app/report.html', context)
