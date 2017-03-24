from django.conf.urls import url

from ClientBank import  views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^add_user/$', views.add_user, name='add_user'),
]
