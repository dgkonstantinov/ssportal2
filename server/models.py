from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from equipment_common.models import BaseEquipment, SlugModelMixin


class Manufacturer(SlugModelMixin):
    name = models.CharField(max_length=48, unique=True, db_index=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=True, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def __str__(self): return self.name

    class Meta: ordering = ['name']; verbose_name = _('Manufacturer'); verbose_name_plural = _('Manufacturers')


class EquipmentModel(SlugModelMixin):
    name = models.CharField(max_length=48, unique=True, db_index=True, verbose_name=_('Name'))
    manufacturer = models.ForeignKey(
        Manufacturer, related_name='server_models',
        on_delete=models.PROTECT, verbose_name=_('Manufacturer')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=True, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def __str__(self): return f"{self.manufacturer.name} {self.name}"

    class Meta: ordering = ['name']; verbose_name = _('Model'); verbose_name_plural = _('Models')


# Chassis must be defined BEFORE Server to resolve FK reference
class Chassis(BaseEquipment):
    CHASSIS_TYPE_CHOICES = [('blade', 'Blade Enclosure'), ('storage', 'Storage Shelf'), ('network', 'Network Chassis')]
    chassis_type = models.CharField(
        max_length=20, choices=CHASSIS_TYPE_CHOICES, default='blade', verbose_name=_('Type')
    )
    slot_count = models.PositiveSmallIntegerField(default=8, verbose_name=_('Slot Count'))
    model = models.ForeignKey(
        EquipmentModel, related_name='chassis_set',
        on_delete=models.PROTECT, verbose_name=_('Equipment model')
    )

    class Meta(BaseEquipment.Meta):
        db_table = 'server_chassis'
        verbose_name = _('Chassis')
        verbose_name_plural = _('Chassis')


class Server(BaseEquipment):
    FORM_FACTOR_CHOICES = [('1U', '1U'), ('2U', '2U'), ('4U', '4U'), ('8U', '8U'), ('Blade', 'Blade'),
                           ('Tower', 'Tower')]
    form_factor = models.CharField(
        max_length=10, choices=FORM_FACTOR_CHOICES, default='2U', verbose_name=_('Form Factor')
    )
    cpu_model = models.CharField(max_length=128, blank=True, verbose_name=_('CPU Model'))
    cpu_count = models.PositiveSmallIntegerField(default=1, verbose_name=_('CPU Count'))
    ram_gb = models.PositiveIntegerField(default=0, verbose_name=_('RAM (GB)'))
    bmc_ip = models.GenericIPAddressField(
        protocol='both', unpack_ipv4=True, blank=True, null=True, verbose_name=_('BMC/IPMI IP')
    )
    model = models.ForeignKey(
        EquipmentModel, related_name='server_set',
        on_delete=models.PROTECT, verbose_name=_('Equipment model')
    )
    chassis = models.ForeignKey(
        Chassis, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='servers', verbose_name=_('Parent Chassis')
    )

    class Meta(BaseEquipment.Meta):
        db_table = 'server_server'
        verbose_name = _('Server')
        verbose_name_plural = _('Servers')


auditlog.register(Manufacturer)
auditlog.register(EquipmentModel)
auditlog.register(Chassis)
auditlog.register(Server)
