from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.dataupload, name='file-upload'),
    url(r'^update/$', views.dataupdate, name='data-update'),
]
