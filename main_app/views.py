from django.shortcuts import render
from .models import Client, ISO3166

# Create your views here.
def index(request, app=None, client_id=None):
	import pdb; pdb.set_trace()

	if app and 'clients' in app:
		return clients(request)
	if app and 'client' in app and 'details' in app:
		return client_details(request, client_id)
	context = {'test':'test'}
	return render(request, 'main_app/index.html', context)


def clients(request):
	country_dict = dict(ISO3166.ISO3166)
	clients_list = [(x.id, x.client_name, country_dict[x.country], x.customer_site, x.start_date) for x in Client.objects.all()]
	context = {'clients_list': clients_list}
	return render(request, 'main_app/clients.html', context)


def client_details(request, client_id):
	import pdb; pdb.set_trace()

	if client_id == 'add':
		pass
	country_dict = dict(ISO3166.ISO3166)
	client_obj = Client.object.get(id=client_id)
	context = {'client_details': client_obj}
	return render(request, 'main_app/clients.html', context)
