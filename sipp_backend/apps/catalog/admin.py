from django.contrib import admin
from .models import Catalog


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('company', 'supplier', 'dataType', 'contractActive', 'created_at')
    list_filter = ('dataType', 'contractActive')
    search_fields = ('company', 'supplier')
    ordering = ('-created_at',)