from django.conf.urls import urls

import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]