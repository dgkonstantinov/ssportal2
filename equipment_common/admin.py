# equipment_common/admin.py
from django.contrib import admin
from .models import EquipmentStatus, PortStatus


@admin.register(EquipmentStatus)
class EquipmentStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'is_protected')
    list_filter = ('is_active', 'is_protected')
    search_fields = ('name', 'slug')
    ordering = ('name',)
    readonly_fields = ('slug', 'created', 'updated')


@admin.register(PortStatus)
class PortStatusAdmin(admin.ModelAdmin):
    # Fixed: removed 'code' as it does not exist in the PortStatus model
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    ordering = ('name',)
    readonly_fields = ('slug', 'created', 'updated')