import django_filters
from rest_framework import viewsets, filters

from .models import Entry
from .serializer import EntrySerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
