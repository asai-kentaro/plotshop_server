from django.contrib import admin

from .models import Entry

@admin.register(Entry)
class Entry(admin.ModelAdmin):
    pass
