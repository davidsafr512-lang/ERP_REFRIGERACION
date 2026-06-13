from django.contrib import admin
from .models import EquipoRefrigeracion

@admin.register(EquipoRefrigeracion)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'ubicacion', 'marca', 'btu', 'refrigerante', 'activo',)
    search_fields = ('tag_id', 'ubicacion', 'marca')
    list_filter = ('marca', 'refrigerante', 'activo')
    def delete_queryset(self, request, queryset):
        queryset.update(activo=False)
    def get_action_choices(self, request, default_choices=None):
        """Sobrescribe las opciones por defecto para eliminar los guiones"""
        return super().get_action_choices(request, default_choices=[])

