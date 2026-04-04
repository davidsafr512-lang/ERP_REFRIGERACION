from django.db import models

class EquipoRefrigeracion(models.Model):
    # Identificador único para el equipo en la planta
    tag_id = models.CharField(max_length=50, unique=True, verbose_name="Código de Inventario")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación Exacta")
    marca = models.CharField(max_length=100)
    
    # Datos Técnicos del Excel
    refrigerante = models.CharField(max_length=50, help_text="Ej: R-410A, R-22")
    voltaje = models.CharField(max_length=20, help_text="Ej: 220V / 110V")
    btu = models.IntegerField(verbose_name="Capacidad (BTU)")
    amperaje = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Amperaje (A)")
    potencia_va = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Potencia (VA)")
    potencia_w = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Potencia (W)")
    
    # Control de Estado
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag_id} - {self.marca} ({self.ubicacion})"

    class Meta:
        verbose_name = "Equipo de Refrigeración"
        verbose_name_plural = "Equipos de Refrigeración"

# --- SISTEMA DE AUDITORÍA ---
from auditlog.registry import auditlog

auditlog.register(EquipoRefrigeracion)