from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^code/(?P<code_id>\d+)/$', views.view, name='view'),
    url(r'^code/(?P<code_id>\d+)/edit$', views.edit, name='edit'),
    url(r'^code/(?P<code_id>\d+)/exec_local$', views.do_exec_local, name='exec_local'),
    url(r'^code/(?P<code_id>\d+)/entry$', views.post_exec, name='entry'),
    url(r'^code/(?P<code_id>\d+)/exec$', views.do_exec, name='exec'),
]
