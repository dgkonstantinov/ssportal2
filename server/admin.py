from django.contrib import admin
from .models import Manufacturer, EquipmentModel, Chassis, Server


class ServerInline(admin.TabularInline):
    model = Server
    fields = ('serial_number', 'form_factor', 'rack_position', 'status', 'is_active')
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('slug', 'created', 'updated')


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'slug', 'is_active')
    list_filter = ('manufacturer',)
    search_fields = ('name',)
    readonly_fields = ('slug', 'created', 'updated')
    autocomplete_fields = ["manufacturer"]


@admin.register(Chassis)
class ChassisAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'chassis_type', 'slot_count', 'status', 'rack')
    list_filter = ('status', 'chassis_type')
    search_fields = ('serial_number', 'model__name')
    readonly_fields = ('datacenter', 'created', 'updated')
    inlines = [ServerInline]
    autocomplete_fields = ["model", "rack", "status"]


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'datacenter', 'rack', 'cpu_count', 'ram_gb', 'status',
                    'is_active', 'is_protected')
    list_filter = ('status', 'form_factor', 'model__manufacturer')
    search_fields = ('serial_number', 'model__name', 'model__manufacturer__name')
    readonly_fields = ('datacenter', 'created', 'updated')
    fieldsets = (
        ('Identification', {'fields': ('model', 'serial_number', 'inventory_number', 'part_number')}),
        ('Location', {'fields': ('rack', 'rack_position', 'rack_units', 'chassis')}),
        ('Hardware', {'fields': ('form_factor', 'cpu_model', 'cpu_count', 'ram_gb', 'bmc_ip')}),
        ('Status & Dates', {'fields': ('status', 'purchase_date', 'warranty_expires')}),
    )
    autocomplete_fields = ["model", "rack", "status", "chassis"]
    # exclude = ['slug', 'created', 'updated']
    list_editable = ('is_active', 'is_protected')
