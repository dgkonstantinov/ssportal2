# datacenter/views.py

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import City, Datacenter, Rack
from .forms import CityForm, DatacenterForm, RackForm


def dashboard(request):
    """Main dashboard view showing overview of cities and datacenters"""
    # Prefetch related objects to avoid N+1 queries
    cities = City.objects.prefetch_related(
        'datacenters__racks'
    ).all()

    datacenters = Datacenter.objects.select_related(
        'city'
    ).prefetch_related(
        'racks'
    ).all()

    context = {
        'cities': cities,
        'datacenters': datacenters,
        'active_section': 'dashboard'
    }
    return render(request, 'datacenter/dashboard.html', context)


# City Views
class CityListView(ListView):
    """List all cities"""
    model = City
    template_name = 'datacenter/city_list.html'
    context_object_name = 'cities'
    ordering = ['name']


class CityCreateView(CreateView):
    """Create new city"""
    model = City
    form_class = CityForm
    template_name = 'datacenter/city_form.html'
    success_url = reverse_lazy('datacenter:city_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать город'
        return context


class CityUpdateView(UpdateView):
    """Update existing city"""
    model = City
    form_class = CityForm
    template_name = 'datacenter/city_form.html'
    success_url = reverse_lazy('datacenter:city_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать город'
        return context


class CityDeleteView(DeleteView):
    """Delete city"""
    model = City
    template_name = 'datacenter/city_confirm_delete.html'
    success_url = reverse_lazy('datacenter:city_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить город'
        return context


# Datacenter Views
class DatacenterListView(ListView):
    """List all datacenters"""
    model = Datacenter
    template_name = 'datacenter/datacenter_list.html'
    context_object_name = 'datacenters'
    ordering = ['name']


class DatacenterCreateView(CreateView):
    """Create new datacenter"""
    model = Datacenter
    form_class = DatacenterForm
    template_name = 'datacenter/datacenter_form.html'
    success_url = reverse_lazy('datacenter:datacenter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать ЦОД'
        return context


class DatacenterUpdateView(UpdateView):
    """Update existing datacenter"""
    model = Datacenter
    form_class = DatacenterForm
    template_name = 'datacenter/datacenter_form.html'
    success_url = reverse_lazy('datacenter:datacenter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать ЦОД'
        return context


class DatacenterDeleteView(DeleteView):
    """Delete datacenter"""
    model = Datacenter
    template_name = 'datacenter/datacenter_confirm_delete.html'
    success_url = reverse_lazy('datacenter:datacenter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить ЦОД'
        return context


# Rack Views
class RackListView(ListView):
    """List all racks"""
    model = Rack
    template_name = 'datacenter/rack_list.html'
    context_object_name = 'racks'
    ordering = ['datacenter', 'name']


class RackCreateView(CreateView):
    """Create new rack"""
    model = Rack
    form_class = RackForm
    template_name = 'datacenter/rack_form.html'
    success_url = reverse_lazy('datacenter:rack_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать стойку'
        return context


class RackUpdateView(UpdateView):
    """Update existing rack"""
    model = Rack
    form_class = RackForm
    template_name = 'datacenter/rack_form.html'
    success_url = reverse_lazy('datacenter:rack_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать стойку'
        return context


class RackDeleteView(DeleteView):
    """Delete rack"""
    model = Rack
    template_name = 'datacenter/rack_confirm_delete.html'
    success_url = reverse_lazy('datacenter:rack_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить стойку'
        return context