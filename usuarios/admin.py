from django.contrib import admin
from .models import Usuario # El nombre exacto de tu modelo

# Esto le dice a Django: "Muestra mi usuario en el panel de control"
admin.site.register(Usuario)