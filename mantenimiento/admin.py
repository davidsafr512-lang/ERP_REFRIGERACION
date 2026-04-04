from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import PlanPreventivo
from django.utils.safestring import mark_safe
from datetime import timedelta
    
@admin.register(PlanPreventivo)
class PlanPreventivoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'criticidad', 'fecha_proximo_mantenimiento', 'estado_mantenimiento')
    list_filter = ('criticidad',)
    readonly_fields = ('fecha_proximo_mantenimiento',)

    # Organizacion de la interfaz en secciones (pestanas visuales)
    fieldsets = (
        ('Información Básica', {
            'fields': ('equipo', 'criticidad', 'frecuencia_dias')
        }),
        ('Checklist de Tareas Obligatorias', {
            'fields': (
                'limpieza_filtros', 'limpieza_evaporadora', 
                'limpieza_condensadora', 'medicion_amperaje', 
                'revision_refrigerante', 'revision_electrica'
            ),
            'description': 'Seleccione las tareas que el técnico debe realizar en este equipo.'
        }),
        ('Cronograma', {
            'fields': ('fecha_ultimo_mantenimiento', 'fecha_proximo_mantenimiento')
        }),
    )

    def estado_mantenimiento(self, obj):
        try:
            if not obj.fecha_proximo_mantenimiento:
                return format_html('<span style="color: gray;">⚪ Sin programar</span>')
            
            import datetime
            hoy = datetime.date.today()
            proxima = obj.fecha_proximo_mantenimiento

            # Forzada la conversión a fecha pura por si acaso
            if isinstance(proxima, str):
                proxima = datetime.datetime.strptime(proxima, '%Y-%m-%d').date()
            elif isinstance(proxima, datetime.datetime):
                proxima = proxima.date()

            diferencia = (proxima - hoy).days

            if diferencia < 0:
                return mark_safe(f'<span style="color: red;">🔴 VENCIDO ({abs(diferencia)} d)</span>')
            elif diferencia <= 7:
                return mark_safe(f'<span style="color: orange;">🟡 POR VENCER ({diferencia} d)</span>')
            else:
                return mark_safe('<span style="color: green;">🟢 AL DÍA</span>')
                
        except Exception as e:
            # LA MAGIA: Si hay error, lo pinta en la tabla y la página no se cae
            return format_html('<span style="color: red;">⚠️ Fallo: {}</span>', str(e))

    estado_mantenimiento.short_description = 'Estado'