from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from .models import Chiller, Chiller_Loop_Pump, Condensate_Pump, Chiller_Images
from .models import Client, CHILLER_TYPE, COMPRESSOR_TYPE

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import ImagesForm

import json
import copy


def index(request):
	try:
		chiller_app_objs = Chiller.objects.all()
	except Exception as exception:
		return Http404('Page not found')
	context = {'chiller_app_objs': chiller_app_objs}
	return render(request, 'chiller_app/index.html', context)


def chiller_loop_pump_selection(chiller_loop_pump_objs, chiller_details_obj):
	if not chiller_loop_pump_objs:
		return None, None

	selected_obj = chiller_loop_pump_objs.filter(selected=True)
	if not selected_obj:
		selected_obj = chiller_loop_pump_objs[0]
		selected_obj.selected = True
		selected_obj.save()
		chiller_loop_pump_objs = Chiller_Loop_Pump.objects.filter(chiller=chiller_details_obj, selected=True)

	chiller_loop_pump_list = [ (x.id, x.chiller_loop_pump_name, x.selected, x.chill_loop_pump) for x in chiller_loop_pump_objs]
	chiller_loop_pump_kw_cost_list = [ (x.chiller_loop_pump_name,
										x.get_chill_loop_info_kwh(),
										x.get_chill_loop_info_cost(),
										x.get_chill_loop_info_kwh(annual_flag=True),
										x.get_chill_loop_info_cost(annual_flag=True),
										x.selected) for x in chiller_loop_pump_objs]

	return chiller_loop_pump_list, chiller_loop_pump_kw_cost_list


def condensate_pump_selection(condensate_pump_objs, chiller_details_obj):
	if not condensate_pump_objs:
		return None, None

	selected_obj = condensate_pump_objs.filter(selected=True)
	if not selected_obj:
		selected_obj = condensate_pump_objs[0]
		selected_obj.selected = True
		selected_obj.save()
		condensate_pump_objs = Condensate_Pump.objects.filter(chiller=chiller_details_obj, selected=True)

	condensate_pump_list = [ (x.id, x.condensate_pump_name, x.selected, x.condensate_pump) for x in condensate_pump_objs]
	condensate_pump_kw_cost_list = [ (x.condensate_pump_name,
									  x.get_condensate_info_kwh(),
									  x.get_condensate_info_cost(),
									  x.get_condensate_info_kwh(annual_flag=True),
									  x.get_condensate_info_cost(annual_flag=True),
									  x.selected) for x in condensate_pump_objs]
	return condensate_pump_list, condensate_pump_kw_cost_list


def get_chill_loop_pump_information_totals(chiller_loop_pump_objs, condensate_pump_objs):
	if not (chiller_loop_pump_objs and condensate_pump_objs):
		return {'chill_loop_pump_total_hp': 0,
				'chill_loop_pump_total_daily_kwh': 0,
				'chill_loop_pump_total_daily_cost': 0,
				'chill_loop_pump_total_annual_kwh': 0,
				'chill_loop_pump_total_annual_cost': 0}


	chiller_loop_pump = chiller_loop_pump_objs.filter(selected=True)[0]
	condensate_pump = condensate_pump_objs.filter(selected=True)[0]
	ret_dict = {
		'chill_loop_pump_total_hp': chiller_loop_pump.chill_loop_pump+condensate_pump.condensate_pump,
		'chill_loop_pump_total_daily_kwh': round(chiller_loop_pump.get_chill_loop_info_kwh()+condensate_pump.get_condensate_info_kwh(), 2),
		'chill_loop_pump_total_daily_cost': round(chiller_loop_pump.get_chill_loop_info_cost()+condensate_pump.get_condensate_info_cost(), 2),
		'chill_loop_pump_total_annual_kwh': round(chiller_loop_pump.get_chill_loop_info_kwh(annual_flag=True)+condensate_pump.get_condensate_info_kwh(annual_flag=True), 2),
		'chill_loop_pump_total_annual_cost': round(chiller_loop_pump.get_chill_loop_info_cost(annual_flag=True)+condensate_pump.get_condensate_info_cost(annual_flag=True), 2)
	}
	return ret_dict


def set_chiller_loop_pump_obj(chiller_obj, chiller_loop_pump_obj):
	Chiller_Loop_Pump.objects.filter(chiller=chiller_obj).update(selected=False)
	selected_obj = Chiller_Loop_Pump.objects.get(id=chiller_loop_pump_obj)
	selected_obj.selected = True
	selected_obj.save()


def set_condensate_pump_obj(chiller_obj, condensate_pump_obj):
	Condensate_Pump.objects.filter(chiller=chiller_obj).update(selected=False)
	selected_obj = Condensate_Pump.objects.get(id=condensate_pump_obj)
	selected_obj.selected = True
	selected_obj.save()


def set_val_chiller_loop_pump(post_key, post_data):
	chiller_loop_pump_id = int(post_key.replace('set_chiller_loop_pump_', ''))
	to_save = Chiller_Loop_Pump.objects.get(id=chiller_loop_pump_id)
	to_save.chill_loop_pump = post_data
	to_save.save()


def set_val_condensate_pump(post_key, post_data):
	condensate_pump_id = int(post_key.replace('set_condensate_pump_', ''))
	to_save = Condensate_Pump.objects.get(id=condensate_pump_id)
	to_save.condensate_pump = post_data
	to_save.save()


def save_chiller_app(request, chiller_id):
	redirect_flag = False
	if chiller_id == 'add':
		chiller_obj = Chiller()
		redirect_flag = True
	else:
		chiller_obj = Chiller.objects.get(id=chiller_id)

	for each in request.POST:
		if each == 'csrfmiddlewaretoken':
			continue
		if each == 'chiller_loop_pump_obj' and chiller_id:
			set_chiller_loop_pump_obj(chiller_obj, request.POST['chiller_loop_pump_obj'])
		if each == 'condensate_pump_obj' and chiller_id:
			set_condensate_pump_obj(chiller_obj, request.POST['condensate_pump_obj'])
		if each.startswith('set_chiller_loop_pump_'):
			set_val_chiller_loop_pump(each, request.POST[each])
			continue
		if each.startswith('set_condensate_pump_'):
			set_val_condensate_pump(each, request.POST[each])
			continue
		if each == 'customer':
			client_obj = Client.objects.get(id=request.POST[each])
			setattr(chiller_obj, 'client', client_obj)
			continue
		setattr(chiller_obj, each, request.POST[each])
	chiller_obj.save()
	return redirect_flag, chiller_obj.id


def save_chiller_loop_pump(request, chiller_id):
	chiller_obj = Chiller.objects.get(id=chiller_id)
	chiller_loop_obj = Chiller_Loop_Pump()
	chiller_loop_obj.chiller = chiller_obj
	chiller_loop_obj.chiller_loop_pump_name = request.POST['chiller_loop_pump_name']
	chiller_loop_obj.chill_loop_pump = request.POST['chill_loop_pump']
	chiller_loop_obj.save()


def save_condensate_pump(request, chiller_id):
	chiller_obj = Chiller.objects.get(id=chiller_id)
	condensate_obj = Condensate_Pump()
	condensate_obj.chiller = chiller_obj
	condensate_obj.condensate_pump_name = request.POST['condensate_pump_name']
	condensate_obj.condensate_pump = request.POST['condensate_pump']
	condensate_obj.save()


def details(request, chiller_id):
	if 'save_chiller_app' in request.POST and request.POST['save_chiller_app'] == '1':
		import pdb; pdb.set_trace()
		redirect_flag, chiller_obj_id = save_chiller_app(request, chiller_id)
		if redirect_flag:
			return redirect('/chiller_app/details/%s/' % (chiller_obj_id,))

	if 'save_chiller_loop_pump' in request.POST and request.POST['save_chiller_loop_pump'] == '1':
		save_chiller_loop_pump(request, chiller_id)

	if 'save_condensate_pump' in request.POST and request.POST['save_condensate_pump'] == '1':
		save_condensate_pump(request, chiller_id)

	if chiller_id != 'add':
		new_chiller_obj = False
		try:
			chiller_details_obj = Chiller.objects.get(id=chiller_id)
		except Exception as exception:
			return Http404('Page not found')

	if chiller_id == 'add':
		chiller_details_obj = Chiller()
		new_chiller_obj = True
		client_objects = Client.objects.all()

	try:
		chiller_loop_pump_objs = Chiller_Loop_Pump.objects.filter(chiller=chiller_details_obj)
		chiller_loop_pump_list, chiller_loop_pump_kw_cost_list = chiller_loop_pump_selection(chiller_loop_pump_objs, chiller_details_obj)
	except Exception as exception:
		return Http404('Page not found')

	try:
		condensate_pump_objs = Condensate_Pump.objects.filter(chiller=chiller_details_obj)
		condensate_pump_list, condensate_pump_kw_cost_list = condensate_pump_selection(condensate_pump_objs, chiller_details_obj)
	except Exception as exception:
		return Http404('Page not found')


	try:
		chiller_images = Chiller_Images.objects.filter(chiller=chiller_details_obj)
	except Exception as exception:
		return Http404('Page not found')


	context = {'chiller_details_obj': chiller_details_obj}
	if chiller_details_obj:
		context_update = {'get_chiller_information_tons_kw': chiller_details_obj.get_chiller_information_tons_kw(),
		'get_chiller_information_m3_hour': chiller_details_obj.get_chiller_information_m3_hour(),
		'get_cooling_tower_temperature_in_and_out_pipe': chiller_details_obj.get_cooling_tower_temperature_in_and_out_pipe(),
		'get_cooling_tower_temperature_oper_display_screen': chiller_details_obj.get_cooling_tower_temperature_oper_display_screen(),
		'get_chiller_loop_temp_in_out_pipe': chiller_details_obj.get_chiller_loop_temp_in_out_pipe(),
		'get_chiller_loop_temp_oper_display_screen': chiller_details_obj.get_chiller_loop_temp_oper_display_screen(),
		'get_chiller_loop_temp_measured_capacity_percent': chiller_details_obj.get_chiller_loop_temp_measured_capacity_percent(),
		'get_chiller_loop_temp_oper_display_screen_percent': chiller_details_obj.get_chiller_loop_temp_oper_display_screen_percent(),
		'get_measured_tons_of_cooling': chiller_details_obj.get_measured_tons_of_cooling(),
		'get_display_tons_of_cooling': chiller_details_obj.get_display_tons_of_cooling(),
		'get_gal_per_min_confirmation_of_chiller_rated_temp_drop': chiller_details_obj.get_gal_per_min_confirmation_of_chiller_rated_temp_drop(),
		'get_nameplate_tons_confirmation_of_chiller_rated_temp_drop': chiller_details_obj.get_nameplate_tons_confirmation_of_chiller_rated_temp_drop(),
		'get_lbs_per_min_confirmation_of_chiller_rated_temp_drop': chiller_details_obj.get_lbs_per_min_confirmation_of_chiller_rated_temp_drop(),
		'get_btu_per_min_confirmation_of_chiller_rated_temp_drop': chiller_details_obj.get_btu_per_min_confirmation_of_chiller_rated_temp_drop(),
		'get_calculated_temp_drop': chiller_details_obj.get_calculated_temp_drop(),
		'get_compare_to_nameplate_rated_temp_drop': chiller_details_obj.get_compare_to_nameplate_rated_temp_drop(),
		'annual_cost_of_operation_kw_during_typical_operation': chiller_details_obj.annual_cost_of_operation_kw_during_typical_operation(),
		'get_cost_of_chiller_operation_only_annualy': chiller_details_obj.get_cost_of_chiller_operation_only_annualy(),
		'get_cost_of_chiller_operation_only_daily': chiller_details_obj.get_cost_of_chiller_operation_only_daily(),
		'get_cost_of_chiller_operation_only_annual_cost': chiller_details_obj.get_cost_of_chiller_operation_only_annual_cost(),
		'chiller_type': CHILLER_TYPE,
		'compressor_type': COMPRESSOR_TYPE,
		'chiller_loop_pump_objs': chiller_loop_pump_list,
		'condensate_pump_objs': condensate_pump_list,
		'chiller_loop_pump_kw_cost_list': chiller_loop_pump_kw_cost_list,
		'condensate_pump_kw_cost_list': condensate_pump_kw_cost_list}
		context.update(context_update)
		info_total = get_chill_loop_pump_information_totals(chiller_loop_pump_objs, condensate_pump_objs)
		context.update(info_total)
		context['total_daily_kwh'] = round(chiller_details_obj.get_cost_of_chiller_operation_only_daily()+
										 info_total['chill_loop_pump_total_daily_kwh'], 2)
		context['total_annual_kwh'] = round(chiller_details_obj.get_cost_of_chiller_operation_only_annualy()+
										 info_total['chill_loop_pump_total_annual_kwh'], 2)
		context['total_annual_cost'] = round(chiller_details_obj.get_cost_of_chiller_operation_only_annual_cost()+
										 info_total['chill_loop_pump_total_annual_cost'], 2)
		context['chiller_images'] = chiller_images
		context['new_chiller_obj'] = new_chiller_obj
		if new_chiller_obj:
			context['client_objects'] = [(x.id, x.client_name) for x in client_objects]

	return render(request, 'chiller_app/details.html', context)


# -*- coding: utf-8 -*-


def images(request, chiller_id):
	# Handle file upload
	import pdb; pdb.set_trace()

	chiller_object = Chiller.objects.get(id=chiller_id)

	if ('save_chiller_image' in request.POST) and (request.method == 'POST'):
		form = ImagesForm(request.POST, request.FILES)
		newimage = Chiller_Images(chiller=chiller_object,
			chiller_images_name=request.POST['image_name'],
			image_description=request.POST['image_description'],
			path_to_image=request.FILES['image_file'])
		newimage.save()
	else:
		form = ImagesForm()
	return redirect('/chiller_app/details/%s/' % (chiller_id,))
