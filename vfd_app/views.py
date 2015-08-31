from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from .models import Client_Vfd_Motor, Client_Vfd_Motor_Data_Per_Month, Materials_Client_VFD_Motor, Labor_Client_VFD_Motor
from django.core.urlresolvers import reverse

import json


MONTHS_ORDER = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
                'OCT', 'NOV', 'DEC']

VFD_SET_POINTS = [100, 90, 80, 70, 60, 50, 40, 30]


def index(request):
    try:
        client_vfd_motor_objs = Client_Vfd_Motor.objects.order_by('-vfd_name')
    except Exception as exception:
        return Http404('Page not found')
    context = {'client_vfd_motor_objs': client_vfd_motor_objs}
    return render(request, 'vfd_app/index.html', context)


class Client_VFD_View(object):
    def __init__(self,
                 client_name=None,
                 vfd_actual_name=None,
                 vfd_name=None,
                 cost_per_kwh=0,
                 installed_date=None,
                 motor_horse_pwr=None,
                 existing_motor_efficiency=None,
                 proposed_vfd_efficiency=None,
                 motor_load=None,
                 monthly_usage=None,
                 monthly_usage_dict=None,
                 vfd_set_point=None):
        self.client_name = client_name
        self.vfd_actual_name = vfd_actual_name
        self.vfd_name = vfd_name
        self.cost_per_kwh = cost_per_kwh
        self.installed_date = installed_date
        self.motor_horse_pwr = motor_horse_pwr
        self.existing_motor_efficiency = existing_motor_efficiency
        self.proposed_vfd_efficiency = proposed_vfd_efficiency
        self.motor_load = motor_load
        self.vfd_set_point = float(vfd_set_point)
        self.monthly_usage = monthly_usage
        self.monthly_usage_dict = monthly_usage_dict
        self.total_hours_of_operation()
        self.total_kwh()
        self.total_cost()
        self.proposed_vfd_kwh()
        self.vfd_belt_kwh()

    def total_hours_of_operation(self):
        self.total_hours_of_operation = sum(
            [x.hours_of_operation for x in self.monthly_usage])

    def total_kwh(self):
        try:
            val = float(1.0/self.existing_motor_efficiency)
            self.total_kwh = self.motor_horse_pwr * val
            self.total_kwh *= self.motor_load
            self.total_kwh *= 0.746
            self.total_kwh *= self.total_hours_of_operation
            self.total_kwh = int(round(self.total_kwh))
        except Exception as exception:
            self.total_kwh = 0

    def total_cost(self):
        self.total_cost = int(round(self.total_kwh * self.cost_per_kwh))

    def proposed_vfd_kwh(self):
        try:
            val_1 = float(1.0/self.existing_motor_efficiency)
            val_2 = float(1.0/self.proposed_vfd_efficiency)
            self.proposed_vfd_kwh = self.total_hours_of_operation
            self.proposed_vfd_kwh *= self.vfd_set_point
            self.proposed_vfd_kwh = int(round(self.proposed_vfd_kwh/100))
            self.proposed_vfd_kwh *= self.vfd_set_point
            self.proposed_vfd_kwh = int(round(self.proposed_vfd_kwh/100))
            self.proposed_vfd_kwh *= self.vfd_set_point
            self.proposed_vfd_kwh *= self.motor_horse_pwr
            self.proposed_vfd_kwh *= float(val_1 * val_2) * 0.746
            self.proposed_vfd_kwh *= self.motor_load
            self.proposed_vfd_kwh = int(round(self.proposed_vfd_kwh))
        except Exception as exception:
            self.proposed_vfd_kwh = 0

    def vfd_belt_kwh(self):
        self.vfd_belt_kwh = int(round(self.proposed_vfd_kwh *
                                      self.cost_per_kwh))


def get_client_vfd_view_obj(client_vfd_id, vfd_set_point):
    client_vfd_obj = Client_Vfd_Motor.objects.get(id=client_vfd_id)
    monthly_usage = Client_Vfd_Motor_Data_Per_Month.objects.filter(
        client_vfd=client_vfd_obj.id, vfd_set_point=vfd_set_point)
    monthly_usage_list = [x for x in monthly_usage]
    monthly_usage_list.sort(key=lambda x: MONTHS_ORDER.index(x.month))
    monthly_usage_dict = {x.month.lower():x.hours_of_operation for x in monthly_usage}
    client_vfd_view_obj = Client_VFD_View(
        client_name=client_vfd_obj.client.client_name,
        vfd_actual_name=client_vfd_obj.vfd.vfd_name,
        vfd_name=client_vfd_obj.vfd_name,
        cost_per_kwh=client_vfd_obj.cost_per_kwh,
        installed_date=client_vfd_obj.installed_date,
        motor_horse_pwr=client_vfd_obj.motor_horse_pwr,
        existing_motor_efficiency=client_vfd_obj.existing_motor_efficiency,
        proposed_vfd_efficiency=client_vfd_obj.proposed_vfd_efficiency,
        motor_load=client_vfd_obj.motor_load,
        monthly_usage=monthly_usage_list,
        monthly_usage_dict=monthly_usage_dict,
        vfd_set_point=vfd_set_point)
    return client_vfd_view_obj


def detail(request, client_vfd_id, vfd_set_point):
    context = {'client_vfd_view': get_client_vfd_view_obj(client_vfd_id,
                                                          vfd_set_point)}
    return render(request, 'vfd_app/detail.html', context)


def search_form(request):
    context = {'data': 'data'}
    return render(request, 'vfd_app/search_form.html', context)


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

    for each_set_point in VFD_SET_POINTS:
        for each_month in MONTHS_ORDER:
            monthly_data_key = '%s_%s' % (each_set_point, each_month.lower())
            try:
                if request.POST[monthly_data_key] and float(request.POST[monthly_data_key].strip()) >= 0:
                    vfd_obj, create = Client_Vfd_Motor_Data_Per_Month.objects.get_or_create(
                        client_vfd=client_vfd_obj,
                        month=each_month,
                        vfd_set_point=each_set_point)

                    vfd_obj.hours_of_operation = float(request.POST[monthly_data_key])
                    vfd_obj.save()
                    if float(request.POST[monthly_data_key]) == 0:
                        vfd_obj.delete()
            except Exception:
                pass
            if not request.POST[monthly_data_key].strip():
                try:
                    montly_obj = Client_Vfd_Motor_Data_Per_Month.objects.get(
                                    client_vfd=client_vfd_obj,
                                    month=each_month,
                                    vfd_set_point=each_set_point)
                    if montly_obj:
                        montly_obj.delete()
                except Exception:
                    pass


def total_kwh(existing_motor_efficiency,
              motor_horse_pwr,
              motor_load,
              total_hours_of_operation
              ):
    try:
        val = float(1.0/existing_motor_efficiency)
        total_kwh = motor_horse_pwr * val
        total_kwh *= motor_load
        total_kwh *= 0.746
        total_kwh *= total_hours_of_operation
        total_kwh = int(round(total_kwh))
    except Exception as exception:
        total_kwh = 0
    return total_kwh

def existing_body_totals(body_dict):
    totals_hours_per_month = {}
    total_hours_of_operation = 0
    for each_month in MONTHS_ORDER:
        totals_hours_per_month.setdefault(each_month.lower(), 0)
        for each_body_data in body_dict['table_body']:
            if each_month.lower() not in each_body_data.keys():
                continue
            totals_hours_per_month[each_month.lower()] += each_body_data[each_month.lower()]
            total_hours_of_operation += each_body_data[each_month.lower()]
    totals_hours_per_month['total_hours_of_operation'] = total_hours_of_operation
    return totals_hours_per_month


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
    if 'save_text' in request.POST and request.POST['save_text'] == '1':
        save_data(request, client_vfd_id)

    if 'save_material' in request.POST and request.POST['save_material'] == '1':
        save_material(request, client_vfd_id)

    if 'save_labor' in request.POST and request.POST['save_labor'] == '1':
        save_labor(request, client_vfd_id)

    table_header = {x.lower():x for x in MONTHS_ORDER}
    table_header['speed'] = 'Speed'
    data = {'table_header': table_header}
    data['table_body'] = []

    total_proposed_vfd_kwh = 0
    total_proposed_cost = 0

    for each_set_point in VFD_SET_POINTS:
        client_vfd_obj = get_client_vfd_view_obj(client_vfd_id, each_set_point)
        body_data = {'speed': each_set_point}
        months_order_lower = [x.lower() for x in MONTHS_ORDER]
        # hours_used = [x.hours_of_operation for x in client_vfd_obj.monthly_usage]
        # body_data.update(dict(zip(months_order_lower, hours_used)))
        body_data.update(client_vfd_obj.monthly_usage_dict)
        body_data['total_hours_of_operation'] = client_vfd_obj.total_hours_of_operation
        body_data['proposed_vfd_kwh'] = client_vfd_obj.proposed_vfd_kwh
        total_proposed_vfd_kwh += client_vfd_obj.proposed_vfd_kwh
        body_data['cost'] = int(round(client_vfd_obj.proposed_vfd_kwh * client_vfd_obj.cost_per_kwh))
        total_proposed_cost += int(round(client_vfd_obj.proposed_vfd_kwh * client_vfd_obj.cost_per_kwh))
        data['table_body'].append(body_data)


    data['client_vfd_id'] = client_vfd_id
    data['client_name'] = client_vfd_obj.client_name
    data['vfd_actual_name'] = client_vfd_obj.vfd_actual_name
    data['vfd_name'] = client_vfd_obj.vfd_name
    data['cost_per_kwh'] = client_vfd_obj.cost_per_kwh
    data['installed_date'] = client_vfd_obj.installed_date
    data['motor_horse_pwr'] = client_vfd_obj.motor_horse_pwr
    data['existing_motor_efficiency'] = client_vfd_obj.existing_motor_efficiency
    data['proposed_vfd_efficiency'] = client_vfd_obj.proposed_vfd_efficiency
    data['motor_load'] = client_vfd_obj.motor_load

    # Existing Motor calculations
    data['existing_motor_header'] = table_header
    data['existing_motor_body'] = []
    existing_motor_body = {'speed': client_vfd_obj.existing_motor_efficiency}
    existing_motor_body.update(existing_body_totals(data))
    existing_kwh_val = total_kwh(client_vfd_obj.existing_motor_efficiency,
                                 client_vfd_obj.motor_horse_pwr,
                                 client_vfd_obj.motor_load,
                                 existing_motor_body['total_hours_of_operation'])
    existing_motor_body['existing_kwh'] = existing_kwh_val
    existing_motor_body['cost'] = int(round(existing_kwh_val * client_vfd_obj.cost_per_kwh))
    data['existing_motor_body'].append(existing_motor_body)

    data['table_footer'] = {'speed': 'Totals'}
    data['table_footer'].update(existing_body_totals(data))
    data['table_footer']['total_proposed_vfd_kwh'] = total_proposed_vfd_kwh
    data['table_footer']['total_proposed_cost'] = total_proposed_cost

    data['existing_kwh'] = existing_kwh_val
    data['existing_cost'] = int(round(existing_kwh_val * client_vfd_obj.cost_per_kwh))

    data['total_proposed_vfd_kwh'] = total_proposed_vfd_kwh
    data['total_proposed_cost'] = total_proposed_cost

    data['annual_kwh_savings'] = existing_kwh_val - total_proposed_vfd_kwh
    data['annual_cost_savings'] = data['existing_cost'] - total_proposed_cost

    data['materials_data'] = installation_pricing_materials(client_vfd_id)
    data['labor_data'] = installation_pricing_labor(client_vfd_id)
    data['project_cost'] = data['materials_data']['total_material_miss_cost'] + data['labor_data']['total_labor_miss_cost']

    import pprint
    pprint.pprint(data)
    context = {'data': data}
    return render(request, 'vfd_app/report.html', context)
