# library/models.py
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
        Manufacturer, related_name='library_models',
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


class TapeLibrary(BaseEquipment):
    TAPE_TECH_CHOICES = [('LTO-7', 'LTO-7'), ('LTO-8', 'LTO-8'), ('LTO-9', 'LTO-9'), ('IBM 3592', 'IBM 3592')]
    tape_tech = models.CharField(
        max_length=20, choices=TAPE_TECH_CHOICES, default='LTO-8', verbose_name=_('Tape Technology')
    )
    drive_count = models.PositiveSmallIntegerField(default=2, verbose_name=_('Drive Count'))
    slot_count = models.PositiveSmallIntegerField(default=20, verbose_name=_('Slot Count'))
    model = models.ForeignKey(
        EquipmentModel, related_name='library_set',
        on_delete=models.PROTECT, verbose_name=_('Equipment model')
    )

    class Meta(BaseEquipment.Meta):
        db_table = 'library_tapelibrary'
        verbose_name = _('Tape Library')
        verbose_name_plural = _('Tape Libraries')


auditlog.register(Manufacturer)
auditlog.register(EquipmentModel)
auditlog.register(TapeLibrary)