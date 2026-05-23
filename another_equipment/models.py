# another_equipment/models.py
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
        Manufacturer, related_name='other_models',
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


class GenericEquipment(BaseEquipment):
    """Fallback model for equipment that doesn't fit specific categories."""
    model = models.ForeignKey(
        EquipmentModel, related_name='other_set',
        on_delete=models.PROTECT, verbose_name=_('Equipment model')
    )

    class Meta(BaseEquipment.Meta):
        db_table = 'anotherequipment_generic'
        verbose_name = _('Other Equipment')
        verbose_name_plural = _('Other Equipment')


auditlog.register(Manufacturer)
auditlog.register(EquipmentModel)
auditlog.register(GenericEquipment)