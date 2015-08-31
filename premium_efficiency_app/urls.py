from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^report/(?P<premium_client_motor_id>[0-9]*)/$', views.report)
]
