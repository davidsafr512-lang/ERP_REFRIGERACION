from django.contrib import admin
from .models import Usuario # El nombre exacto del modelo

class UsuarioAdmin(admin.ModelAdmin):
    # Este es el mismo método que usaste en los otros modelos
    def get_action_choices(self, request, default_choices=None):
        return super().get_action_choices(request, default_choices=[])

# Registramos el modelo vinculado a su nueva clase de configuración
admin.site.register(Usuario, UsuarioAdmin)