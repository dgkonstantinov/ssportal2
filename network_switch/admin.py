from django.contrib import admin
from .models import Manufacturer, EquipmentModel, NetworkSwitch, NetworkSwitchPort


class NetworkSwitchPortInline(admin.TabularInline):
    model = NetworkSwitchPort
    fields = ('slot', 'port', 'status', 'description')
    extra = 0


@admin.register(NetworkSwitch)
class NetworkSwitchAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'port_count', 'management_ip', 'poe_support', 'status', 'rack')
    list_filter = ('status', 'poe_support', 'model__manufacturer')
    search_fields = ('serial_number', 'model__name')
    readonly_fields = ('datacenter', 'created', 'updated')
    inlines = [NetworkSwitchPortInline]


@admin.register(NetworkSwitchPort)
class NetworkSwitchPortAdmin(admin.ModelAdmin):
    list_display = ('switch', 'slot', 'port', 'status')
    list_filter = ('status', 'switch__model__manufacturer')
    search_fields = ('switch__serial_number', 'description')
    ordering = ('switch', 'slot', 'port')