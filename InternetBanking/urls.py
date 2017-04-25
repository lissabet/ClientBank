from django.conf.urls import url, include
from InternetBanking import  views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from InternetBanking.views import UserList, UsersDetail, InfoList, InfoDetail

urlpatterns = [

    url(r'^$', views.my_view, name='my_view'),
    url(r'^users/(?P<pk>\d+)/$', UsersDetail.as_view(), name='user-detail'),
    url(r'^groups/$', InfoList.as_view(), name='info-list'),
    url(r'^groups/(?P<pk>\d+)/$', InfoDetail.as_view(), name='info-detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name ='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'InternetBanking/login.html'}),
    url(r'index/$',views.index,name='index'),
    url(r'profile/$',views.profile, name='profile'),
    url(r'create_product/$',views.CreateProduct, name='create_product'),
    url(r'warring/$', views.warring, name='warring'),
    url(r'nomoney/$', views.nomoney, name='nomoney'),
    url(r'phone_operation/$',views.phone_operation,name='phone_operation'),
    url(r'operations/$',views.operations,name='operations'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
