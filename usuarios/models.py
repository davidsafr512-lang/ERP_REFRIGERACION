from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Definimos los 3 niveles de acceso
    ADMIN = 'ADMIN'
    SUPERVISOR = 'SUPER'
    TECNICO = 'TEC'
    
    ROLES_CHOICES = [
        (ADMIN, 'Administrador de Sistema'),
        (SUPERVISOR, 'Supervisor de Mantenimiento'),
        (TECNICO, 'Técnico de Refrigeración'),
    ]

    rol = models.CharField(
        max_length=10, 
        choices=ROLES_CHOICES, 
        default=TECNICO
    )
    
    # Un campo útil para saber a quién contactar
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
