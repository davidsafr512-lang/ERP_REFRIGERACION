from django.contrib import admin
from .models import ReporteServicio

@admin.register(ReporteServicio)
class ReporteServicioAdmin(admin.ModelAdmin):
    def get_action_choices(self, request, default_choices=None):
        """Sobrescribe las opciones por defecto para eliminar los guiones"""
        return super().get_action_choices(request, default_choices=[])
    
    def get_readonly_fields(self, request, obj=None):
        """Bloquea los campos una vez que el reporte ha sido guardado en la base de datos"""
        if obj:  # Si 'obj' no es None, significa que el registro ya existe y se está editando
            # Aquí pones la lista EXACTA de campos de tu modelo que quieres congelar
            return ['plan', 'fecha_ejecucion', 'tecnico_responsable', 'amperaje_leido', 'presion_alta', 'presion_baja', 'tareas_completadas', 'observaciones']
        
        # Si el reporte es NUEVO, dejamos el campo 'usuario' como solo lectura 
        # para que nadie pueda suplantar la identidad de otro compañero al crearlo
        return ['usuario', 'fecha_ejecucion']

    def save_model(self, request, obj, form, change):
        """Captura automáticamente al usuario logueado que está creando el reporte"""
        if not change:  # Si el registro es completamente nuevo (no una edición)
            obj.usuario = request.user  # Asigna al técnico o administrador actual
        super().save_model(request, obj, form, change)

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