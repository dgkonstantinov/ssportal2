# server/urls.py
from django.urls import path
from . import views

app_name = 'server'

urlpatterns = [
    # Servers
    path('servers/', views.server_list, name='server_list'),
    path('servers/create/', views.server_create, name='server_create'),
    path('servers/<int:pk>/edit/', views.server_update, name='server_update'),  # ← Исправлено
    path('servers/<int:pk>/delete/', views.server_delete, name='server_delete'),  # ← Исправлено
    # path('servers/<int:pk>/files/', views.server_files, name='server_files'),  # ← Исправлено
    # path('servers/<int:pk>/files/upload/', views.file_upload, name='file_upload'),  # ← Исправлено
    # path('servers/<int:pk>/files/<int:file_id>/delete/', views.file_delete, name='file_delete'),  # ← Исправлено

    # Chassis
    path('chassis/', views.chassis_list, name='chassis_list'),
    path('chassis/create/', views.chassis_create, name='chassis_create'),
    path('chassis/<int:pk>/edit/', views.chassis_update, name='chassis_update'),
    path('chassis/<int:pk>/delete/', views.chassis_delete, name='chassis_delete'),
]