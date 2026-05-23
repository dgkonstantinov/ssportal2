from django.urls import path
from . import views

app_name = 'datacenter'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # City URLs
    path('cities/', views.CityListView.as_view(), name='city_list'),
    path('cities/create/', views.CityCreateView.as_view(), name='city_create'),
    path('cities/<slug:slug>/edit/', views.CityUpdateView.as_view(), name='city_update'),
    path('cities/<slug:slug>/delete/', views.CityDeleteView.as_view(), name='city_delete'),

    # Datacenter URLs
    path('datacenters/', views.DatacenterListView.as_view(), name='datacenter_list'),
    path('datacenters/create/', views.DatacenterCreateView.as_view(), name='datacenter_create'),
    path('datacenters/<slug:slug>/edit/', views.DatacenterUpdateView.as_view(), name='datacenter_update'),
    path('datacenters/<slug:slug>/delete/', views.DatacenterDeleteView.as_view(), name='datacenter_delete'),

    # Rack URLs
    path('racks/', views.RackListView.as_view(), name='rack_list'),
    path('racks/create/', views.RackCreateView.as_view(), name='rack_create'),
    path('racks/<slug:slug>/edit/', views.RackUpdateView.as_view(), name='rack_update'),
    path('racks/<slug:slug>/delete/', views.RackDeleteView.as_view(), name='rack_delete'),
]