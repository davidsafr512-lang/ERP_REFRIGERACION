from django.contrib import admin
from .models import EquipoRefrigeracion

@admin.register(EquipoRefrigeracion)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'ubicacion', 'marca', 'btu', 'refrigerante')
    search_fields = ('tag_id', 'ubicacion', 'marca')
    list_filter = ('marca', 'refrigerante')