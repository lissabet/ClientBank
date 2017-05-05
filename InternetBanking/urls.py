from django.conf.urls import url, include
from InternetBanking import  views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^$', views.my_view, name='my_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name ='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'InternetBanking/login.html'}),
    url(r'index/$',views.index,name='index'),
    url(r'profile/$',views.profile, name='profile'),
    url(r'export_product/$', views.product_export, name='export_product'),
    url(r'create_product/$',views.CreateProduct, name='create_product'),
    url(r'warring/$', views.warring, name='warring'),
    url(r'nomoney/$', views.nomoney, name='nomoney'),
    url(r'phone_operation/$',views.phone_operation,name='phone_operation'),
    url(r'operations/$',views.operations,name='operations'),
    url(r'internet_pay/$',views.internet_pay,name='internet_pay'),
    url(r'flat_pay/$',views.flat_pay,name='flat_pay'),
    url(r'keys/$',views.keysView,name='keys'),
    url(r'export_phone/$',views.export_phone,name='export_phone'),
    url(r'export_internet/$',views.export_internet,name='export_internet'),
    url(r'export_flatpay/$', views.export_flatpay, name='export_flatpay'),
    url(r'archive/$', views.archive, name='archive'),
    url(r'products/$', views.products, name='products'),
    url(r'edit/$', views.edit ,name='edit'),
    url(r'stop/$',views.stop,name='stop'),
    url(r'active/$',views.active,name='active')


]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
