from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.dataupload, name='file-upload'),
    url(r'^update/$', views.dataupdate, name='data-update'),
    url(r'^link/view/(?P<data_id>\d+)/$', views.link, name='link-view'),
    url(r'^link/add/$', views.linkadd, name='link-add'),
]
