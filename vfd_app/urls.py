from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /vfd_app/
    url(r'^$', views.index, name='index'),
    # ex: /vfd_app/5/
    url(r'^(?P<client_vfd_id>[0-9]+)/(?P<vfd_set_point>[0-9]+)/$', views.detail, name='detail'),
    # Submit Request
    url(r'^report/(?P<client_vfd_id>[0-9]*)/$', views.report),
]
