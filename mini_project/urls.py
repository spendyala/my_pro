"""mini_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^(|/|(?P<app>clients/)|(?P<comment>comment/)|client/details/(?P<client_id>([0-9]+|add))/)$', include('main_app.urls', namespace='main_app')),
	# url(r'^(|/)$', include('main_app.urls', namespace='main_app')),
	url(r'^vfd_app/', include('vfd_app.urls', namespace='vfd_app')),
	url(r'^premium_efficiency_app/', include('premium_efficiency_app.urls', namespace='premium_efficiency_app')),
	url(r'^chiller_app/', include('chiller_app.urls', namespace='permium_efficiency_app')),
	# url(r'^test_angular/', include('test_angular.urls')),
]
