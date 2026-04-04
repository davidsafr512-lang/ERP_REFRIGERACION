#!/usr/bin/env bash
# Salir si hay error
set -o errexit

pip install -r requirements.txt

# Recolectar estáticos (Logo, CSS, Chart.js)
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos de la nube
python manage.py migrate