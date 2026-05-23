from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from utils.tools import create_slug


class SlugModelMixin(models.Model):
    """Provides auto-generated slug on first save."""
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Slug'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        super().save(*args, **kwargs)


class EquipmentStatus(SlugModelMixin):
    name = models.CharField(max_length=48, unique=True, db_index=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=True, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Equipment status')
        verbose_name_plural = _('Equipment statuses')


class PortStatus(SlugModelMixin):
    """Replaces the old STATUS_CHOICES tuple for switch ports."""
    name = models.CharField(max_length=48, unique=True, db_index=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Port status')
        verbose_name_plural = _('Port statuses')


class BaseEquipment(models.Model):
    """Abstract base containing fields shared across all hardware types."""
    inventory_number = models.CharField(
        max_length=64, unique=True, blank=True, null=True, db_index=True,
        verbose_name=_('Inventory number'),
        help_text=_('Unique accounting identifier. Optional on create.')
    )
    serial_number = models.CharField(max_length=64, unique=True, verbose_name=_('Serial number'))
    part_number = models.CharField(max_length=64, blank=True, verbose_name=_('Part Number'))
    status = models.ForeignKey(
        'equipment_common.EquipmentStatus', related_name='%(class)s_set',
        on_delete=models.PROTECT, verbose_name=_('Status')
    )
    purchase_date = models.DateField(_('Purchase Date'), null=True, blank=True)
    warranty_expires = models.DateField(_('Warranty Expires'), null=True, blank=True)
    rack = models.ForeignKey(
        'datacenter.Rack', related_name='%(class)s_set',
        null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('Rack')
    )
    rack_position = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None, verbose_name=_('Rack Position (U)')
    )
    rack_units = models.PositiveSmallIntegerField(
        blank=True, default=1, verbose_name=_('Height (U)')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=False, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    # inherit=True creates separate history tables for each concrete subclass
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        ordering = ['-created']
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    @property
    def datacenter(self):
        """Computed property. Always syncs with rack.datacenter."""
        return self.rack.datacenter if self.rack_id else None

    def clean(self):
        super().clean()
        if self.rack_position is not None and self.rack_position < 1:
            raise ValidationError({'rack_position': _('Position must be >= 1')})
        if self.rack_units is not None and self.rack_units < 1:
            raise ValidationError({'rack_units': _('Height must be >= 1')})

    def __str__(self):
        mfr = self.model.manufacturer.name if self.model and self.model.manufacturer else 'Unknown'
        mdl = self.model.name if self.model else 'Unknown'
        return f"{mfr} {mdl} ({self.serial_number})"


# Audit registration for shared models
auditlog.register(EquipmentStatus)
auditlog.register(PortStatus)