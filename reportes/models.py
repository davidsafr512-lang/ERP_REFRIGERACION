from django.db import models
from mantenimiento.models import PlanPreventivo

class ReporteServicio(models.Model):
    # Enlazamos el reporte a un plan específico
    plan = models.ForeignKey(PlanPreventivo, on_delete=models.CASCADE, verbose_name="Equipo en Plan")
    fecha_ejecucion = models.DateField(auto_now_add=True)
    
    # Datos Técnicos encontrados en el sitio
    amperaje_leido = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Amperaje Medido (A)")
    presion_alta = models.FloatField(verbose_name="Presión Alta (PSI)", null=True, blank=True)
    presion_baja = models.FloatField(verbose_name="Presión Baja (PSI)", null=True, blank=True)
    
    # Observaciones del técnico
    observaciones = models.TextField(blank=True, null=True)
    tareas_completadas = models.TextField(help_text="Ej: Limpieza de filtros, lavado de serpentín")
    
    # Firma digital (nombre de quien lo hizo)
    tecnico_responsable = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # LA MAGIA: Al guardar el reporte, se actualiza la fecha en el Plan Preventivo
        super().save(*args, **kwargs)
        plan = self.plan
        plan.fecha_ultimo_mantenimiento = self.fecha_ejecucion
        plan.save() # Esto disparará el cálculo automático de la próxima fecha que hicimos antes

    class Meta:
        verbose_name = "Reporte de Servicio"
        verbose_name_plural = "Reportes de Servicio"