from django.db import models

# 1. Crea esta función ANTES de tu clase EquipoRefrigeracion
def generar_codigo_ref():
    # Importamos el modelo aquí dentro para que Python no se queje de que la clase aún no ha sido leída
    from .models import EquipoRefrigeracion 
    
    # Buscamos el último equipo que se guardó en la base de datos
    ultimo_equipo = EquipoRefrigeracion.objects.order_by('id').last()
    
    if not ultimo_equipo or not ultimo_equipo.tag_id:
        # Si es una base de datos limpia y no hay equipos, empezamos por el 1
        return 'REF-001'
    
    # Extraemos el código actual (ejemplo: 'REF-043')
    codigo_anterior = ultimo_equipo.tag_id
    try:
        # Separamos el texto por el guion y tomamos la parte numérica
        numero = int(codigo_anterior.split('-')[1])
        nuevo_numero = numero + 1
        
        # Retornamos el nuevo código forzando a que tenga 3 dígitos (ej: 044)
        return f'REF-{nuevo_numero:03d}'
    except (IndexError, ValueError):
        # Un respaldo de seguridad por si algún código manual anterior no tiene el formato correcto
        return 'REF-000'
    
class EquipoRefrigeracion(models.Model):
    # Identificador único para el equipo en la planta
    tag_id = models.CharField(max_length=20, unique=True, default=generar_codigo_ref, verbose_name="Código de Inventario")
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

# 1. Añadimos el nuevo campo de estado
    activo = models.BooleanField(
        default=True, 
        verbose_name="Equipo Activo",
        help_text="Desmarca esta casilla en lugar de borrar el equipo para mantener el historial."
    )

    # 2. Sobrescribimos el método de borrado individual
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()
        
    def __str__(self):
        return f"{self.tag_id} - {self.marca} ({self.ubicacion})"

    class Meta:
        verbose_name = "Equipo de Refrigeración"
        verbose_name_plural = "Equipos de Refrigeración"

# --- SISTEMA DE AUDITORÍA ---
from auditlog.registry import auditlog

auditlog.register(EquipoRefrigeracion)