from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^exec/', views.do_exec_local),
    url(r'^execbreak/', views.exec_code_with_breakout, name="api_code_breakout"),
    url(r'^code/(?P<code_id>\d+)/load$', views.load_code, name='api_code'),
    url(r'^code/(?P<code_id>\d+)/meta$', views.post_meta, name='api_meta'),
    url(r'^data/csv$', views.load_csv, name='api_data_csv'),
]
