# library/admin.py
from django.contrib import admin
from .models import Manufacturer, EquipmentModel, TapeLibrary


@admin.register(TapeLibrary)
class TapeLibraryAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'tape_tech', 'slot_count', 'status', 'rack')
    list_filter = ('status', 'tape_tech', 'model__manufacturer')
    search_fields = ('serial_number', 'model__name')
    readonly_fields = ('datacenter', 'created', 'updated')