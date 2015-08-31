from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /vfd_app/
	url(r'^$', views.index, name='index'),
	# ex: /vfd_app/5/
	url(r'^details/(?P<chiller_id>([0-9]+|add))/$', views.details, name='details'),
	# url(r'^images/$', views.images , name='images'),
	url(r'^images/(?P<chiller_id>([0-9]+))/$', views.images , name='images'),
]
