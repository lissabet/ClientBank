from django.conf.urls import url, include
from InternetBanking import views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^$', views.my_view, name='my_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'base.html'}),
    url(r'index/$', views.index, name='index'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'export_product/$', views.product_export, name='export_product'),
    url(r'create_product/$', views.CreateProduct, name='create_product'),
    url(r'warring/$', views.warring, name='warring'),
    url(r'nomoney/$', views.nomoney, name='nomoney'),
    url(r'phone_operation/$', views.phone_operation, name='phone_operation'),
    url(r'operations/$', views.operations, name='operations'),
    url(r'internet_pay/$', views.internet_pay, name='internet_pay'),
    url(r'flat_pay/$', views.flat_pay, name='flat_pay'),
    url(r'keys/$', views.keysView, name='keys'),
    url(r'export_phone/$', views.export_phone, name='export_phone'),
    url(r'export_internet/$', views.export_internet, name='export_internet'),
    url(r'export_flatpay/$', views.export_flatpay, name='export_flatpay'),
    url(r'archive/$', views.archive, name='archive'),
    url(r'products/$', views.products, name='products'),
    url(r'edit/$', views.edit, name='edit'),
    url(r'stop/$', views.stop, name='stop'),
    url(r'active/$', views.active, name='active'),
    url(r'change_password/$', views.change_password, name='change_password'),
    url(r'code/$', views.code, name='code'),
    url(r'new_password/$', views.new_password, name='new_password'),
    url(r'successfully_password/$', views.successfully_password, name='successfully_password'),
    url(r'money_transfer/$',views.money_transfer,name='money_transfer'),
    url(r'transfer_export/$',views.transfer_export,name='transfer_export'),
    url(r'statistics/$', views.statistics_money_transfer, name='statistics'),
    url(r'all_users/$', views.list_admin_users, name='all_users'),
    url(r'administration/$', views.administration, name='administration'),
    url(r'user_detail/$', views.detail_user, name='user_detail'),

]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
