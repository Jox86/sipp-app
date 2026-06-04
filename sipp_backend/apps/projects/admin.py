from django.contrib import admin
from .models import Project, BudgetHistory


class BudgetHistoryInline(admin.TabularInline):
    model = BudgetHistory
    extra = 0
    readonly_fields = ('budget', 'period', 'periodEnd', 'syncedAt')
    can_delete = False
    max_num = 10


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('costCenter', 'projectNumber', 'name', 'owner', 'budget', 'area', 'status', 'renewalDate')
    list_filter = ('status', 'areaType', 'area')
    search_fields = ('costCenter', 'projectNumber', 'name', 'owner__fullName', 'owner__email')
    ordering = ('-created_at',)
    inlines = [BudgetHistoryInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('name', 'description', 'costCenter', 'projectNumber')
        }),
        ('Presupuesto', {
            'fields': ('budget', 'budgetPeriod', 'renewalDate', 'endDate')
        }),
        ('Ubicación', {
            'fields': ('area', 'areaType')
        }),
        ('Responsable y Estado', {
            'fields': ('owner', 'status')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(BudgetHistory)
class BudgetHistoryAdmin(admin.ModelAdmin):
    list_display = ('project', 'budget', 'period', 'periodEnd', 'syncedAt')
    list_filter = ('period',)
    search_fields = ('project__costCenter', 'project__projectNumber')
    readonly_fields = ('project', 'budget', 'period', 'periodEnd', 'syncedAt')
