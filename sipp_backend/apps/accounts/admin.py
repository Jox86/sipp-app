from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'fullName', 'role', 'area', 'areaType', 'is_active', 'created_at')
    list_filter = ('role', 'areaType', 'is_active')
    search_fields = ('email', 'fullName', 'area')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informacion Personal', {'fields': ('email', 'fullName', 'password')}),
        ('Rol y Area', {'fields': ('role', 'area', 'areaType')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('created_at', 'updated_at', 'last_login')}),
    )
    add_fieldsets = (
        ('Nuevo Usuario', {
            'classes': ('wide',),
            'fields': ('email', 'fullName', 'password1', 'password2', 'role', 'area', 'areaType'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
