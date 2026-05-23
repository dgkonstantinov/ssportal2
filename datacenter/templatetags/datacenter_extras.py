from django import template

register = template.Library()


@register.filter
def racks_count(datacenters):
    """Count total racks across all datacenters"""
    return sum(dc.racks.count() for dc in datacenters.all())
