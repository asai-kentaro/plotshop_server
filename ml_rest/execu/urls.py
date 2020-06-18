from execu import views
from django.conf.urls import url

urlpatterns = [
    url(r'^exec/', views.execution),
    url(r'^list/(?P<code_id>\d+)', views.entry_list),
]
