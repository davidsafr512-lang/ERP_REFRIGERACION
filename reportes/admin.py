from django.contrib import admin
from .models import ReporteServicio

@admin.register(ReporteServicio)
class ReporteServicioAdmin(admin.ModelAdmin):
    # Columnas que se verán en el listado principal
    list_display = ('plan', 'fecha_ejecucion', 'tecnico_responsable', 'amperaje_leido')
    
    # Filtros laterales para encontrar reportes rápido
    list_filter = ('fecha_ejecucion', 'tecnico_responsable')
    
    # Buscador por el código del equipo (tag_id) o el nombre del técnico
    search_fields = ('plan__equipo__tag_id', 'tecnico_responsable')
    
    # Campo de fecha como solo lectura (porque Django la pone automáticamente)
    readonly_fields = ('fecha_ejecucion',)

    # Organización de los campos al abrir un reporte
    fieldsets = (
        ('Información General', {
            'fields': ('plan', 'tecnico_responsable', 'fecha_ejecucion')
        }),
        ('Datos Técnicos (Mediciones)', {
            'fields': ('amperaje_leido', 'presion_alta', 'presion_baja')
        }),
        ('Resultados del Trabajo', {
            'fields': ('tareas_completadas', 'observaciones')
        }),
    )