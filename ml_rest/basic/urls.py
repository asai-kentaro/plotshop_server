from rest_framework import routers
from .views import EntryViewSet


router = routers.DefaultRouter()
router.register(r'entries', EntryViewSet)
