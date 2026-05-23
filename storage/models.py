# storage/models.py
from django.db import models
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
        Manufacturer, related_name='storage_models',
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


class StorageSystem(BaseEquipment):
    STORAGE_TYPE_CHOICES = [('SAN', 'SAN'), ('NAS', 'NAS'), ('DAS', 'DAS'), ('HCI', 'Hyperconverged')]
    storage_type = models.CharField(
        max_length=20, choices=STORAGE_TYPE_CHOICES, default='SAN', verbose_name=_('Type')
    )
    raw_capacity_tb = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name=_('Raw Capacity (TB)'))
    usable_capacity_tb = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name=_('Usable Capacity (TB)'))
    controller_ips = models.JSONField(default=list, blank=True, verbose_name=_('Controller IPs'))
    model = models.ForeignKey(
        EquipmentModel, related_name='storage_set',
        on_delete=models.PROTECT, verbose_name=_('Equipment model')
    )

    class Meta(BaseEquipment.Meta):
        db_table = 'storage_system'
        verbose_name = _('Storage System')
        verbose_name_plural = _('Storage Systems')


auditlog.register(Manufacturer)
auditlog.register(EquipmentModel)
auditlog.register(StorageSystem)