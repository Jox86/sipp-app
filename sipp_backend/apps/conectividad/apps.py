# apps/conectividad/apps.py
from django.apps import AppConfig

class ConectividadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.conectividad'
    label = 'conectividad'  # Asegurar label único
    verbose_name = 'Conectividad'