from django.conf.urls import url

from . import views

app_name = 'inspector'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<player_id>[0-9]+)$', views.detail, name='detail'),
	url(r'^ausencias$', views.ausencias, name='ausencias'),
]
