from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^code/(?P<code_id>\d+)/$', views.view_code, name='view'),
    url(r'^code/(?P<code_id>\d+)/edit$', views.edit_code, name='edit'),
    url(r'^code/(?P<code_id>\d+)/exec_local$', views.do_exec_local, name='exec_local'),
]
