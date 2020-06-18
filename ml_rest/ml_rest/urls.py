from django.conf.urls import url, include
from django.contrib import admin

from basic.urls import router as basic_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # blog.urlsをincludeする
    url(r'^api/', include(basic_router.urls)),
    url(r'^code/', include(('execu.urls', 'execu'), namespace='execu')),
]
