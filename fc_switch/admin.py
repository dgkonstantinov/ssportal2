from django.contrib import admin
from .models import Manufacturer, EquipmentModel, FCSwitch, FCSwitchPort


class FCSwitchPortInline(admin.TabularInline):
    model = FCSwitchPort
    fields = ('slot', 'port', 'status', 'description')
    extra = 0


@admin.register(FCSwitch)
class FCSwitchAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'port_speed', 'management_ip', 'status', 'rack')
    list_filter = ('status', 'port_speed', 'model__manufacturer')
    search_fields = ('serial_number', 'model__name')
    readonly_fields = ('datacenter', 'created', 'updated')
    inlines = [FCSwitchPortInline]


@admin.register(FCSwitchPort)
class FCSwitchPortAdmin(admin.ModelAdmin):
    list_display = ('switch', 'slot', 'port', 'status')
    list_filter = ('status', 'switch__model__manufacturer')
    search_fields = ('switch__serial_number', 'description')
    ordering = ('switch', 'slot', 'port')