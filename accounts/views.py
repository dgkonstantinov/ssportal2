from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
import csv
from datetime import datetime


def is_admin(user):
    """Check if user is administrator"""
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Administrators').exists())


class CustomLoginView(LoginView):
    """Custom login view with redirect"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('datacenter:dashboard')


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = 'accounts:login'


@login_required
@user_passes_test(is_admin, login_url='datacenter:dashboard')
def user_create(request):
    """Create new user (admin only)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        group_name = request.POST.get('group')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('accounts:user_create')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff
        )

        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        messages.success(request, f'Пользователь {username} успешно создан.')
        return redirect('accounts:user_list')

    groups = Group.objects.all()
    return render(request, 'accounts/user_form.html', {'groups': groups})


@login_required
@user_passes_test(is_admin, login_url='datacenter:dashboard')
def user_list(request):
    """List all users (admin only)"""
    users = User.objects.all().prefetch_related('groups')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@user_passes_test(is_admin, login_url='datacenter:dashboard')
def user_edit(request, pk):
    """Edit user (admin only)"""
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.is_active = request.POST.get('is_active') == 'on'

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()

        # Update groups
        group_name = request.POST.get('group')
        user.groups.clear()
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        messages.success(request, f'Пользователь {user.username} обновлен.')
        return redirect('accounts:user_list')

    groups = Group.objects.all()
    return render(request, 'accounts/user_edit.html', {'user_obj': user, 'groups': groups})


@login_required
@user_passes_test(is_admin, login_url='datacenter:dashboard')
def user_delete(request, pk):
    """Delete user (admin only)"""
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Пользователь {user.username} удален.')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_confirm_delete.html', {'user_obj': user})


@login_required
@user_passes_test(is_admin, login_url='datacenter:dashboard')
def export_cities_csv(request):
    """Export cities to CSV"""
    from datacenter.models import City

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=cities_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.write('\ufeff')  # BOM for Excel

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Название', 'Описание', 'ЦОДы', 'Стойки', 'Статус', 'Создан'])

    cities = City.objects.prefetch_related('datacenters__racks').all()
    for city in cities:
        total_racks = sum(dc.racks.count() for dc in city.datacenters.all())
        writer.writerow([
            city.name,
            city.description,
            city.datacenters.count(),
            total_racks,
            'Активен' if city.is_active else 'Неактивен',
            city.created.strftime('%d.%m.%Y %H:%M')
        ])

    return response


@login_required
@user_passes_test(is_admin, login_url='datacenter:dashboard')
def export_datacenters_csv(request):
    """Export datacenters to CSV"""
    from datacenter.models import Datacenter

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=datacenters_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Название', 'Город', 'Адрес', 'Стойки', 'Статус', 'Создан'])

    datacenters = Datacenter.objects.select_related('city').prefetch_related('racks').all()
    for dc in datacenters:
        writer.writerow([
            dc.name,
            dc.city.name if dc.city else '-',
            dc.address,
            dc.racks.count(),
            'Активен' if dc.is_active else 'Неактивен',
            dc.created.strftime('%d.%m.%Y %H:%M')
        ])

    return response