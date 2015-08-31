from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from .models import Premium_Efficiency_Client_Motor

import json


MONTHS_ORDER = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
                'OCT', 'NOV', 'DEC']

VFD_SET_POINTS = [100, 90, 80, 70, 60, 50, 40, 30]


def index(request):
    try:
        premium_efficiency_motor_objs = Premium_Efficiency_Client_Motor.objects.order_by('-motor_name')
    except Exception as exception:
        return Http404('Page not found')
    context = {'premium_efficiency_motor_objs': premium_efficiency_motor_objs}
    return render(request, 'premium_efficiency_app/index.html', context)


def full_load_energy_cost(motor_nameplate_hp, annual_operating_hours, energy_cost, load_efficiency, load_val=1):
    try:
        val = (motor_nameplate_hp * 0.746 * annual_operating_hours *
                    energy_cost * load_val * 100)
        val = round(val/load_efficiency)
        return val
    except Exception as exception:
        return 0


def report(request, premium_client_motor_id):
    premium_client_motor = Premium_Efficiency_Client_Motor.objects.get(id=premium_client_motor_id)
    premium_client_motor_obj = {}
    premium_client_motor_obj['client'] = premium_client_motor.client.client_name
    premium_client_motor_obj['motor_name'] = premium_client_motor.motor_name
    premium_client_motor_obj['annual_operating_hours'] = premium_client_motor.annual_operating_hours
    premium_client_motor_obj['energy_cost'] = premium_client_motor.energy_cost
    premium_client_motor_obj['motor_nameplate_hp'] = premium_client_motor.motor_nameplate_hp
    premium_client_motor_obj['existing_full_load_eff'] = premium_client_motor.existing_full_load_eff
    premium_client_motor_obj['existing_three_fourth_load_eff'] = premium_client_motor.existing_three_fourth_load_eff
    premium_client_motor_obj['existing_half_load_eff'] = premium_client_motor.existing_half_load_eff
    premium_client_motor_obj['existing_motor_purchase_price'] = premium_client_motor.existing_motor_purchase_price
    premium_client_motor_obj['proposed_full_load_eff'] = premium_client_motor.proposed_full_load_eff
    premium_client_motor_obj['proposed_three_fourth_load_eff'] = premium_client_motor.proposed_three_fourth_load_eff
    premium_client_motor_obj['proposed_half_load_eff'] = premium_client_motor.proposed_half_load_eff
    premium_client_motor_obj['proposed_motor_purchase_price'] = premium_client_motor.proposed_motor_purchase_price

    premium_client_motor_obj['purchase_difference'] = (premium_client_motor.proposed_motor_purchase_price -
                                                       premium_client_motor.existing_motor_purchase_price)

    premium_client_motor_obj['existing_energy_cost_full_load'] = full_load_energy_cost(
        premium_client_motor.motor_nameplate_hp,
        premium_client_motor.annual_operating_hours,
        premium_client_motor.energy_cost,
        premium_client_motor.existing_full_load_eff
    )
    premium_client_motor_obj['proposed_energy_cost_full_load'] = full_load_energy_cost(
        premium_client_motor.motor_nameplate_hp,
        premium_client_motor.annual_operating_hours,
        premium_client_motor.energy_cost,
        premium_client_motor.proposed_full_load_eff
    )
    premium_client_motor_obj['existing_energy_cost_three_fourth_load'] = full_load_energy_cost(
        premium_client_motor.motor_nameplate_hp,
        premium_client_motor.annual_operating_hours,
        premium_client_motor.energy_cost,
        premium_client_motor.existing_three_fourth_load_eff,
        load_val=0.75
    )
    premium_client_motor_obj['proposed_energy_cost_three_fourth_load'] = full_load_energy_cost(
        premium_client_motor.motor_nameplate_hp,
        premium_client_motor.annual_operating_hours,
        premium_client_motor.energy_cost,
        premium_client_motor.proposed_three_fourth_load_eff,
        load_val=0.75
    )
    premium_client_motor_obj['existing_energy_cost_half_load'] = full_load_energy_cost(
        premium_client_motor.motor_nameplate_hp,
        premium_client_motor.annual_operating_hours,
        premium_client_motor.energy_cost,
        premium_client_motor.existing_half_load_eff,
        load_val=0.5
    )
    premium_client_motor_obj['proposed_energy_cost_half_load'] = full_load_energy_cost(
        premium_client_motor.motor_nameplate_hp,
        premium_client_motor.annual_operating_hours,
        premium_client_motor.energy_cost,
        premium_client_motor.proposed_half_load_eff,
        load_val=0.5
    )
    premium_client_motor_obj['motor_nameplate_rpm'] = premium_client_motor.motor_nameplate_rpm
    premium_client_motor_obj['annual_cost_diff_full_load'] = (premium_client_motor_obj['existing_energy_cost_full_load'] -
                                                              premium_client_motor_obj['proposed_energy_cost_full_load'])
    premium_client_motor_obj['annual_cost_diff_three_fourth_load'] = (premium_client_motor_obj['existing_energy_cost_three_fourth_load'] -
                                                                      premium_client_motor_obj['proposed_energy_cost_three_fourth_load'])
    premium_client_motor_obj['annual_cost_diff_half_load'] = (premium_client_motor_obj['existing_energy_cost_half_load'] -
                                                              premium_client_motor_obj['proposed_energy_cost_half_load'])

    context = {'premium_client_motor_obj': premium_client_motor_obj}
    return render(request, 'premium_efficiency_app/report.html', context)
