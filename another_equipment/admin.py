# another_equipment/admin.py
from django.contrib import admin
from .models import Manufacturer, EquipmentModel, GenericEquipment


@admin.register(GenericEquipment)
class GenericEquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'status', 'rack', 'rack_position', 'is_active')
    list_filter = ('status', 'is_active', 'model__manufacturer')
    search_fields = ('serial_number', 'model__name')
    readonly_fields = ('datacenter', 'created', 'updated')