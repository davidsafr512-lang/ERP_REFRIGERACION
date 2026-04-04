#!/usr/bin/env bash
# Salir si hay error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos (Logo, CSS, etc)
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos de Render
python manage.py migrate