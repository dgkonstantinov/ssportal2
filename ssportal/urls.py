from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('datacenter/', include('datacenter.urls', namespace='datacenter')),
    path('server/', include('server.urls', namespace='server')),  # ← Добавьте эту строку

    # При необходимости подключите другие приложения:
    # path('network_switch/', include('network_switch.urls', namespace='network_switch')),
    # path('fc_switch/', include('fc_switch.urls', namespace='fc_switch')),
]
