from django.contrib import admin

# Register your models here.
from .models import (Client_Vfd_Motor,
					 Client_Vfd_Motor_Data_Per_Month,
					 Materials_Client_VFD_Motor,
					 Labor_Client_VFD_Motor,
					 Client_Vfd_Motor_Setpoint_Selections)


class ClientVfdAdmin(admin.ModelAdmin):
	list_display = ('vfd_name', 'client', 'installed_date', 'was_recent')
	fieldsets = [
		(None, {'fields': ['vfd_name',
						   'client',
						   'cost_per_kwh']}),
		('More information', {'fields': ['vfd',
										 'installed_date',
										 'motor_horse_pwr',
										 'existing_motor_efficiency',
										 'proposed_vfd_efficiency',
										 'motor_load']})
	]


class ClientVfdMonthAdmin(admin.ModelAdmin):
	list_filter = ['month', 'client_vfd']
	list_display = ('client_vfd', 'month', 'hours_of_operation')
	fieldset = [
		(None, {'fields': ['client_vfd', 'month', 'hours_of_operation']})]


class ClientVfdMaterialAdmin(admin.ModelAdmin):
	list_filter = ['item', 'client_vfd']
	list_display = ('quantity', 'item', 'client_vfd', 'ges_cost_each', 'ges_markup')
	# fieldset


class ClientVfdLaborAdmin(admin.ModelAdmin):
	list_filter = ['item', 'client_vfd']
	list_display = ('quantity', 'item', 'client_vfd', 'hourly_rate', 'fixed_cost', 'ges_cost', 'ges_markup', 'fixed_flag')


admin.site.register(Client_Vfd_Motor, ClientVfdAdmin)
admin.site.register(Client_Vfd_Motor_Data_Per_Month, ClientVfdMonthAdmin)
admin.site.register(Materials_Client_VFD_Motor, ClientVfdMaterialAdmin)
admin.site.register(Labor_Client_VFD_Motor, ClientVfdLaborAdmin)
admin.site.register(Client_Vfd_Motor_Setpoint_Selections)
