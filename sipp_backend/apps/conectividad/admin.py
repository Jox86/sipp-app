from django.contrib import admin
from .models import ServicioConectividad


@admin.register(ServicioConectividad)
class ServicioConectividadAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'titular', 'cargo', 'area', 'telefono', 'email', 'activo', 'created_at')
    list_filter = ('tipo', 'activo')
    search_fields = ('titular', 'area', 'email')
    ordering = ('-created_at',)