import os
import django

# Configuramos el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    # Cambia estos datos por los que quieras usar
    username = 'admin_pollo'
    email = 'admin@pollopremium.com'
    password = 'TuPasswordSeguro123' # Pon una clave real aquí

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado exitosamente.")
    else:
        print(f"⚠️ El usuario '{username}' ya existe.")

if __name__ == "__main__":
    create_superuser()