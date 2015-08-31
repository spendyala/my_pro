from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /main_app/
	url(r'^$', views.index, name='index'),
	# url(r'^details/(?P<client_id>([0-9]+|add))$', views.client_details, name="client_details")
]
