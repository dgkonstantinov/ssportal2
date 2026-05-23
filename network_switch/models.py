from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from equipment_common.models import BaseEquipment, SlugModelMixin, PortStatus


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
        Manufacturer, related_name='network_switch_models',
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


class NetworkSwitch(BaseEquipment):
    os_version = models.CharField(max_length=64, blank=True, verbose_name=_('OS Version'))
    management_ip = models.GenericIPAddressField(
        protocol='both', unpack_ipv4=True, blank=True, null=True, verbose_name=_('Management IP')
    )
    port_count = models.PositiveSmallIntegerField(verbose_name=_('Port Count'), default=24)
    poe_support = models.BooleanField(default=False, verbose_name=_('PoE Support'))
    model = models.ForeignKey(
        EquipmentModel, related_name='network_switch_set',
        on_delete=models.PROTECT, verbose_name=_('Equipment model')
    )

    class Meta(BaseEquipment.Meta):
        db_table = 'networkswitch_switch'
        verbose_name = _('Network Switch')
        verbose_name_plural = _('Network Switches')


class NetworkSwitchPort(models.Model):
    switch = models.ForeignKey(
        NetworkSwitch, related_name='ports', on_delete=models.CASCADE, verbose_name=_('Network Switch')
    )
    slot = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Slot Number'))
    port = models.PositiveSmallIntegerField(verbose_name=_('Port Number'))
    status = models.ForeignKey(
        'equipment_common.PortStatus', on_delete=models.PROTECT, verbose_name=_('Status')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords(inherit=True)

    class Meta:
        db_table = 'networkswitch_port'
        ordering = ['slot', 'port']
        verbose_name = _('Network Port')
        verbose_name_plural = _('Network Ports')
        constraints = [
            models.UniqueConstraint(fields=['switch', 'slot', 'port'], name='unique_network_port')
        ]

    @property
    def identifier(self):
        return f"{self.slot}/{self.port}" if self.slot is not None else str(self.port)

    def clean(self):
        super().clean()
        if self.port < 1:
            raise ValidationError({'port': _('Port number must be >= 1')})
        if self.slot is not None and self.slot < 1:
            raise ValidationError({'slot': _('Slot number must be >= 1')})

    def __str__(self):
        return f"{self.switch} :: {self.identifier}"


auditlog.register(Manufacturer)
auditlog.register(EquipmentModel)
auditlog.register(NetworkSwitch)
auditlog.register(NetworkSwitchPort)