from django.contrib import admin
from .models import City, Datacenter, Rack, DCIM


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin interface for managing cities."""
    list_display = ('name', 'is_active', 'is_protected')
    list_filter = ('is_active', 'is_protected')
    search_fields = ('name', 'slug')
    ordering = ('name',)
    # readonly_fields = ('slug', 'created', 'updated')
    fieldsets = (
        ('General', {'fields': ('name', 'slug')}),
        ('Details', {'fields': ('description', 'is_active', 'is_protected')}),
        ('Timestamps', {'fields': ('created', 'updated'), 'classes': ('collapse',)}),
    )
    exclude = ['slug', 'created', 'updated']
    list_editable = ('is_active', 'is_protected')


@admin.register(Datacenter)
class DatacenterAdmin(admin.ModelAdmin):
    """Admin interface for managing data centers."""
    list_display = ('name', 'city', 'address', 'is_active', 'is_protected')
    list_filter = ('city', 'is_active', 'is_protected')
    search_fields = ('name', 'address')
    ordering = ('name',)
    readonly_fields = ('slug', 'created', 'updated')
    fieldsets = (
        ('General', {'fields': ('name', 'slug', 'city')}),
        ('Location & Details', {'fields': ('address', 'description')}),
        ('Status', {'fields': ('is_active', 'is_protected')}),
        ('Timestamps', {'fields': ('created', 'updated'), 'classes': ('collapse',)}),
    )
    autocomplete_fields = ["city", ]
    exclude = ['slug', 'created', 'updated']
    list_editable = ('is_active', 'is_protected')


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    """Admin interface for managing server racks."""
    list_display = ('name', 'datacenter', 'units_count', 'inventory_number', 'power_capacity_kw',
                    'is_active', 'is_protected')
    list_filter = ('datacenter', 'is_active', 'is_protected')
    search_fields = ('name', 'slug', 'inventory_number')
    ordering = ('datacenter', 'name')
    readonly_fields = ('slug', 'created', 'updated')
    fieldsets = (
        ('General', {'fields': ('name', 'slug', 'datacenter')}),
        ('Specifications', {'fields': ('units_count', 'inventory_number', 'power_capacity_kw')}),
        ('Details', {'fields': ('description', 'is_active', 'is_protected')}),
        ('Timestamps', {'fields': ('created', 'updated'), 'classes': ('collapse',)}),
    )
    autocomplete_fields = ["datacenter"]
    exclude = ['slug', 'created', 'updated']
    list_editable = ('is_active', 'is_protected')


@admin.register(DCIM)
class DCIMAdmin(admin.ModelAdmin):
    """Admin interface for DCIM software integrations."""
    list_display = ('name', 'slug', 'fqdn', 'ip_address', 'is_active', 'is_protected')
    list_filter = ('is_active', 'is_protected')
    search_fields = ('name', 'slug', 'fqdn', 'ip_address')
    ordering = ('name',)
    readonly_fields = ('slug', 'created', 'updated')
    fieldsets = (
        ('General', {'fields': ('name', 'slug')}),
        ('Connection', {'fields': ('fqdn', 'ip_address')}),
        ('Details', {'fields': ('description', 'is_active', 'is_protected')}),
        ('Timestamps', {'fields': ('created', 'updated'), 'classes': ('collapse',)}),
    )
    empty_value_display = "unknown"
