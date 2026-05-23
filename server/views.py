from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
import csv
from datetime import datetime
from .models import Server, Chassis


def is_admin(user):
    """Check if user has administrative privileges"""
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Administrators').exists())


# ==========================================
# SERVER VIEWS
# ==========================================
@login_required
def server_list(request):
    """List servers with status filtering"""
    filter_type = request.GET.get('filter', 'all')
    queryset = Server.objects.select_related(
        'model__manufacturer', 'status', 'rack__datacenter', 'chassis'
    ).all()

    if filter_type == 'active':
        queryset = queryset.filter(is_active=True)
    elif filter_type == 'reserve':
        queryset = queryset.filter(is_active=False)

    context = {
        'servers': queryset.order_by('-created'),
        'active_filter': filter_type,
        'title': 'Серверы'
    }
    return render(request, 'server/server_list.html', context)


@login_required
@user_passes_test(is_admin, login_url='server:server_list')
def server_create(request):
    """Create new server"""
    if request.method == 'POST':
        # Handle form validation & saving here
        messages.success(request, 'Сервер успешно создан.')
        return redirect('server:server_list')
    return render(request, 'server/server_form.html', {'title': 'Создание сервера'})


@login_required
@user_passes_test(is_admin, login_url='server:server_list')
def server_update(request, pk):
    """Update existing server"""
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        messages.success(request, 'Сервер успешно обновлен.')
        return redirect('server:server_list')
    return render(request, 'server/server_form.html', {'title': 'Редактирование сервера', 'server': server})


@login_required
@user_passes_test(is_admin, login_url='server:server_list')
def server_delete(request, pk):
    """Delete server"""
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        server.delete()
        messages.success(request, 'Сервер удален.')
        return redirect('server:server_list')
    return render(request, 'server/server_confirm_delete.html', {'server': server})


@login_required
@user_passes_test(is_admin, login_url='server:server_list')
def server_export(request):
    """Export servers to CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=servers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.write('\ufeff')  # UTF-8 BOM for Excel compatibility

    writer = csv.writer(response, delimiter=';')
    writer.writerow(
        ['Серийный номер', 'Модель', 'Производитель', 'Форм-фактор', 'CPU', 'RAM', 'ЦОД', 'Стойка', 'Статус'])

    for s in Server.objects.select_related('model__manufacturer', 'rack__datacenter').all():
        writer.writerow([
            s.serial_number, s.model.name, s.model.manufacturer.name, s.form_factor,
            f"{s.cpu_count}x {s.cpu_model or '-'}", f"{s.ram_gb} GB",
            s.rack.datacenter.name if s.rack and s.rack.datacenter else '-',
            s.rack.name if s.rack else '-', 'Активен' if s.is_active else 'В резерве'
        ])
    return response


# ==========================================
# CHASSIS VIEWS
# ==========================================
@login_required
def chassis_list(request):
    """List chassis with annotated server count"""
    chassis_qs = Chassis.objects.select_related(
        'model__manufacturer', 'status', 'rack__datacenter'
    ).annotate(server_count=Count('servers')).order_by('-created')

    return render(request, 'server/chassis_list.html', {'chassis_list': chassis_qs, 'title': 'Шасси'})


@login_required
@user_passes_test(is_admin, login_url='server:chassis_list')
def chassis_create(request):
    if request.method == 'POST':
        messages.success(request, 'Шасси успешно создано.')
        return redirect('server:chassis_list')
    return render(request, 'server/chassis_form.html', {'title': 'Создание шасси'})


@login_required
@user_passes_test(is_admin, login_url='server:chassis_list')
def chassis_update(request, pk):
    chassis = get_object_or_404(Chassis, pk=pk)
    if request.method == 'POST':
        messages.success(request, 'Шасси успешно обновлено.')
        return redirect('server:chassis_list')
    return render(request, 'server/chassis_form.html', {'title': 'Редактирование шасси', 'chassis': chassis})


@login_required
@user_passes_test(is_admin, login_url='server:chassis_list')
def chassis_delete(request, pk):
    chassis = get_object_or_404(Chassis, pk=pk)
    if request.method == 'POST':
        chassis.delete()
        messages.success(request, 'Шасси удалено.')
        return redirect('server:chassis_list')
    return render(request, 'server/chassis_confirm_delete.html', {'chassis': chassis})


@login_required
@user_passes_test(is_admin, login_url='server:chassis_list')
def chassis_export(request):
    """Export chassis to CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=chassis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow(
        ['Серийный номер', 'Модель', 'Производитель', 'Тип', 'Слоты', 'ЦОД', 'Стойка', 'Серверов', 'Статус'])

    qs = Chassis.objects.select_related('model__manufacturer', 'rack__datacenter').annotate(
        server_count=Count('servers'))
    for c in qs:
        writer.writerow([
            c.serial_number, c.model.name, c.model.manufacturer.name, c.get_chassis_type_display(),
            c.slot_count, c.rack.datacenter.name if c.rack and c.rack.datacenter else '-',
            c.rack.name if c.rack else '-', c.server_count, 'Активно' if c.is_active else 'Неактивно'
        ])
    return response