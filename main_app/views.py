from django.shortcuts import render, redirect
from .models import Client, ISO3166

import datetime

# Create your views here.
def index(request, app=None, client_id=None):
	if app and 'clients' in app:
		return clients(request)
	if client_id:
		return client_details(request, client_id)
	context = {'test':'test'}
	return render(request, 'main_app/index.html', context)


def clients(request):
	country_dict = dict(ISO3166.ISO3166)
	clients_list = [(x.id, x.client_name, country_dict[x.country], x.customer_site, x.start_date) for x in Client.objects.all()]
	context = {'clients_list': clients_list,
			   'country_dict': ISO3166.ISO3166}
	return render(request, 'main_app/clients.html', context)


def save_client_app(request, client_id):
	new_object = False
	if client_id == 'add':
		new_object = True
		client_obj = Client()
		client_obj.start_date = datetime.datetime.now()
	else:
		client_obj = Client.objects.get(id=client_id)

	client_obj.client_name = request.POST['client_name']
	client_obj.country = request.POST['country']
	client_obj.customer_site = request.POST['customer_site']
	client_obj.save()
	return new_object, client_obj.id


def client_details(request, client_id):
	new_object = False
	if 'save_client_app' in request.POST and request.POST['save_client_app'] == '1':
		new_object, client_id = save_client_app(request, client_id)

	if new_object:
		return redirect('/clients/')

	country_dict = dict(ISO3166.ISO3166)
	client_obj = Client.objects.get(id=client_id)
	context = {'client_id': client_obj.id,
		'client_name': client_obj.client_name,
		'country': client_obj.country,
		'customer_site': client_obj.customer_site,
		'start_date': client_obj.start_date,
		'country_dict': ISO3166.ISO3166}
	return render(request, 'main_app/client_details.html', context)
