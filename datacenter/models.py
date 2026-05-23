from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from utils.tools import create_slug


class City(models.Model):
    name = models.CharField(max_length=48, unique=True, db_index=True, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=False, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Generate or update slug only if it's empty or the name has changed
        new_slug = create_slug(self.name)
        if not self.slug or self.slug != new_slug:
            self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city_show', kwargs={'slug': self.slug})

    def total_racks_count(self):
        """Calculate total racks across all datacenters in this city"""
        total = 0
        for dc in self.datacenters.all():
            total += dc.racks.count()
        return total

    def total_servers_count(self):
        """Calculate total servers across all racks in this city"""
        # Placeholder - will be implemented when server app is ready
        return 0

    class Meta:
        ordering = ['name']
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Datacenter(models.Model):
    name = models.CharField(max_length=48, unique=True, db_index=True, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Slug'))
    city = models.ForeignKey(
        City, related_name='datacenters',
        null=True, blank=True, on_delete=models.PROTECT,
        verbose_name=_('City')
    )
    address = models.CharField(max_length=128, blank=True, verbose_name=_('Address'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=False, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        new_slug = create_slug(self.name)
        if not self.slug or self.slug != new_slug:
            self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('datacenter_show', kwargs={'slug': self.slug})

    def total_racks_count(self):
        """Get total racks count (cached property)"""
        return self.racks.count()

    class Meta:
        ordering = ['name']
        verbose_name = _('Data center')
        verbose_name_plural = _('Data centers')


class Rack(models.Model):
    name = models.CharField(max_length=48, db_index=True, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Slug'))
    units_count = models.PositiveIntegerField(
        verbose_name=_('Units (U)'), default=42,
        validators=[MinValueValidator(1), MaxValueValidator(48)],
        help_text=_('Allowed: 1U to 48U')
    )
    inventory_number = models.CharField(
        max_length=64, verbose_name=_('Inventory number'), unique=True,
        blank=True, null=True, db_index=True,
        help_text=_('Unique accounting identifier. Optional on create.')
    )
    power_capacity_kw = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_('Power (kW)'), blank=True, null=True,
        validators=[MinValueValidator(0)], help_text=_('Max allowable power per rack, e.g. 3.50')
    )
    datacenter = models.ForeignKey(
        Datacenter, related_name='racks', on_delete=models.PROTECT,
        verbose_name=_('Data center')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=False, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Generate slug only if both datacenter and name are assigned
        if self.datacenter_id and self.name:
            # Combine datacenter slug and rack name for global uniqueness
            base_slug = f"{self.datacenter.slug}-{self.name}"
            new_slug = create_slug(base_slug)
            if not self.slug or self.slug != new_slug:
                self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rack_show', kwargs={'slug': self.slug})

    class Meta:
        # Order by datacenter first to prevent ambiguity when rack names are not unique
        ordering = ['datacenter', 'name']
        verbose_name = _('Rack')
        verbose_name_plural = _('Racks')


class DCIM(models.Model):
    name = models.CharField(max_length=16, unique=True, db_index=True, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Slug'))
    fqdn = models.CharField(max_length=48, null=True, blank=True, verbose_name=_('FQDN'))
    ip_address = models.CharField(max_length=45, unique=True, verbose_name=_('IP address'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_protected = models.BooleanField(default=True, verbose_name=_('Protected from modification'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        new_slug = create_slug(self.name)
        if not self.slug or self.slug != new_slug:
            self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dcim_show', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = _('DCIM Software')
        verbose_name_plural = _('DCIM Software')


# Register models for audit logging
auditlog.register(City)
auditlog.register(Datacenter)
auditlog.register(Rack)
auditlog.register(DCIM)
