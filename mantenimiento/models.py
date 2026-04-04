from django.db import models
from datetime import timedelta
from inventario.models import EquipoRefrigeracion
import datetime

class PlanPreventivo(models.Model):
    CRITICIDAD_CHOICES = [
        ('ALTA', 'Alta (30 días)'),
        ('MEDIA', 'Media (60 días)'),
        ('BAJA', 'Baja (90 días)'),
    ]
    
    # Relación y Prioridad
    equipo = models.OneToOneField(EquipoRefrigeracion, on_delete=models.CASCADE, verbose_name="Equipo")
    criticidad = models.CharField(max_length=10, choices=CRITICIDAD_CHOICES, default='MEDIA')
    frecuencia_dias = models.PositiveIntegerField(
        null=True, blank=True, 
        help_text="Si se deja vacío, se usará la frecuencia por defecto de la criticidad"
    )

    # --- CHECKLIST TÉCNICO (Tareas a realizar) ---
    limpieza_filtros = models.BooleanField(default=True, verbose_name="¿Limpieza de Filtros?")
    limpieza_evaporadora = models.BooleanField(default=True, verbose_name="¿Limpieza de Evaporadora?")
    limpieza_condensadora = models.BooleanField(default=True, verbose_name="¿Limpieza de Condensadora?")
    medicion_amperaje = models.BooleanField(default=True, verbose_name="¿Medición de Amperaje?")
    revision_refrigerante = models.BooleanField(default=True, verbose_name="¿Revisión de Gas Refrigerante?")
    revision_electrica = models.BooleanField(default=True, verbose_name="¿Revisión de Conexiones Eléctricas?")

    # Control de Fechas
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True, verbose_name="Último Mantenimiento")
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True, verbose_name="Próximo Mantenimiento (Auto)")

    def save(self, *args, **kwargs):
        # 1. Asignar frecuencia automática si está vacía
        if not self.frecuencia_dias:
            if self.criticidad == 'ALTA': self.frecuencia_dias = 30
            elif self.criticidad == 'MEDIA': self.frecuencia_dias = 60
            else: self.frecuencia_dias = 90

        # 2. Cálculo de fecha a prueba de balas
        try:
            if self.fecha_ultimo_mantenimiento:
                # Convertimos la variable a fecha pura sin importar cómo venga
                fecha_base = self.fecha_ultimo_mantenimiento
                
                if isinstance(fecha_base, str):
                    # Si Django la pasa como texto ('YYYY-MM-DD')
                    fecha_base = datetime.datetime.strptime(fecha_base, '%Y-%m-%d').date()
                elif isinstance(fecha_base, datetime.datetime):
                    # Si la pasa con horas y minutos
                    fecha_base = fecha_base.date()

                # Ahora sí, hacemos la matemática segura
                self.fecha_proximo_mantenimiento = fecha_base + datetime.timedelta(days=int(self.frecuencia_dias))
            else:
                self.fecha_proximo_mantenimiento = None
        except Exception as e:
            # Si algo falla en el cálculo, lo imprimimos en la terminal de VS Code pero NO rompemos el programa
            print(f"🔥 ERROR EN SAVE (models.py): {e}")
            self.fecha_proximo_mantenimiento = None
            
        super(PlanPreventivo, self).save(*args, **kwargs)

    def __str__(self):
        return f"Plan: {self.equipo.tag_id} ({self.criticidad})"

    class Meta:
        verbose_name = "Plan Preventivo"
        verbose_name_plural = "Planes Preventivos"

# --- SISTEMA DE AUDITORÍA ---
from auditlog.registry import auditlog

# Registramos el modelo para que Django guarde el historial de cambios
auditlog.register(PlanPreventivo)