from django.contrib import admin

# Register your models here.
from .models import Client, Vfd, Comments


class ClientAdmin(admin.ModelAdmin):
	# fields = ['client_name', 'country', 'start_date']
	list_filter = ['start_date', 'country']
	list_display = ('client_name', 'country', 'start_date', 'was_recent')
	fieldsets = [
		(None,               {'fields': ['client_name']}),
		('More information', {'fields': ['country', 'customer_site', 'start_date'],
							  'classes': ['collapse']}),
	]


class VfdAdmin(admin.ModelAdmin):
	# fields = ['client_name', 'country', 'start_date']
	list_filter = ['vfd_install_date']
	list_display = ('vfd_name',
					# 'cost_per_kwh',
					'vfd_install_date',
					'recent_install')
	fieldsets = [
		(None,               {'fields': ['vfd_name',
										 'vfd_install_date']}),
	]


admin.site.register(Client, ClientAdmin)
admin.site.register(Vfd, VfdAdmin)
admin.site.register(Comments)
