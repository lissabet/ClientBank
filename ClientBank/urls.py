from django.conf.urls import url
from ClientBank import  views
from rest_framework.urlpatterns import format_suffix_patterns
from ClientBank.views import UserList, UsersDetail, InfoList, InfoDetail

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', UsersDetail.as_view(), name='user-detail'),
    url(r'^groups/$', InfoList.as_view(), name='info-list'),
    url(r'^groups/(?P<pk>\d+)/$', InfoDetail.as_view(), name='info-detail'),
    url(r'^register/$', views.register, name='register'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
