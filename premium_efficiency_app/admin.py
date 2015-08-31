from django.contrib import admin

# Register your models here.
from .models import Premium_Efficiency_Client_Motor


class Premium_Efficiency_Client_Motor_Admin(admin.ModelAdmin):
    list_filter = ['client']
    list_display = ('motor_name',
                    'client',
                    'annual_operating_hours',
                    'energy_cost',
                    'motor_nameplate_hp',

                    'existing_full_load_eff',
                    'existing_motor_purchase_price',

                    'proposed_full_load_eff',
                    'proposed_motor_purchase_price',)


admin.site.register(Premium_Efficiency_Client_Motor, Premium_Efficiency_Client_Motor_Admin)
