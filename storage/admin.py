# storage/admin.py
from django.contrib import admin
from .models import Manufacturer, EquipmentModel, StorageSystem


@admin.register(StorageSystem)
class StorageSystemAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'storage_type', 'usable_capacity_tb', 'status', 'rack')
    list_filter = ('status', 'storage_type', 'model__manufacturer')
    search_fields = ('serial_number', 'model__name')
    readonly_fields = ('datacenter', 'created', 'updated')
    fieldsets = (
        ('Identification', {'fields': ('model', 'serial_number', 'inventory_number')}),
        ('Location', {'fields': ('rack', 'rack_position', 'rack_units')}),
        ('Capacity', {'fields': ('storage_type', 'raw_capacity_tb', 'usable_capacity_tb', 'controller_ips')}),
        ('Status', {'fields': ('status', 'purchase_date', 'warranty_expires')}),
    )