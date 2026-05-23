from django import forms
from .models import City, Datacenter, Rack


class CityForm(forms.ModelForm):
    """Form for creating and editing cities"""
    class Meta:
        model = City
        fields = ['name', 'description', 'is_active', 'is_protected']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название города'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_protected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DatacenterForm(forms.ModelForm):
    """Form for creating and editing datacenters"""
    class Meta:
        model = Datacenter
        fields = ['name', 'city', 'address', 'description', 'is_active', 'is_protected']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название ЦОД'
            }),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_protected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RackForm(forms.ModelForm):
    """Form for creating and editing racks"""
    class Meta:
        model = Rack
        fields = ['name', 'datacenter', 'units_count', 'inventory_number',
                  'power_capacity_kw', 'description', 'is_active', 'is_protected']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название стойки'
            }),
            'datacenter': forms.Select(attrs={'class': 'form-select'}),
            'units_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 48
            }),
            'inventory_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Инвентарный номер'
            }),
            'power_capacity_kw': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '3.50'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_protected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }