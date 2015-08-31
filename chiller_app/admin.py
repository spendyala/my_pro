from django.contrib import admin

from .models import Chiller, Chiller_Loop_Pump, Condensate_Pump, Chiller_Images
# Register your models here.
class ChillerAdmin(admin.ModelAdmin):
	list_filter = ['client']
	list_display = ('project_name',
					'client',
					'chiller_name',
					'chiller_model_number',
					'chiller_type',)


class CondenserPumpAdmin(admin.ModelAdmin):
	list_filter = ['chiller']
	list_display = ('chiller', 'condensate_pump', 'condensate_pump_name', 'selected')


class ChillerLoopPumpAdmin(admin.ModelAdmin):
	list_filter = ['chiller']
	list_display = ('chiller', 'chill_loop_pump', 'chiller_loop_pump_name', 'selected')

class Chiller_ImagesAdmin(admin.ModelAdmin):
	list_filter = ['chiller']
	list_display = ('chiller', 'path_to_image')


admin.site.register(Chiller, ChillerAdmin)
admin.site.register(Chiller_Loop_Pump, ChillerLoopPumpAdmin)
admin.site.register(Condensate_Pump, CondenserPumpAdmin)
admin.site.register(Chiller_Images, Chiller_ImagesAdmin)
