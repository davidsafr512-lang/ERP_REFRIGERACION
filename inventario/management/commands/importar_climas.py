import csv
from django.core.management.base import BaseCommand
from inventario.models import EquipoRefrigeracion

class Command(BaseCommand):
    help = 'Carga equipos desde un CSV con encabezados estandarizados'

    def add_arguments(self, parser):
        parser.add_argument('archivo_csv', type=str, help='Ruta al archivo CSV')

    def handle(self, *args, **options):
        ruta = options['archivo_csv']
        
        try:
            # 'utf-8-sig' maneja posibles carácteres ocultos de Excel
            with open(ruta, encoding='utf-8-sig') as f:
                # Usamos el delimitador punto y coma según tu archivo
                reader = csv.DictReader(f, delimiter=';')
                count = 0
                
                for row in reader:
                    # Si el tag_id viene vacío en el Excel, lo generamos
                    id_celda = row.get('tag_id', '').strip()
                    if not id_celda:
                        tag_id_final = f"REF-{str(count + 1).zfill(3)}"
                    else:
                        tag_id_final = id_celda

                    # Función interna rápida para limpiar números con coma (ej: 2,5 -> 2.5)
                    def limpiar_num(valor):
                        if not valor: return 0.0
                        return float(str(valor).replace(',', '.'))

                    # Guardar o actualizar en la base de datos
                    EquipoRefrigeracion.objects.update_or_create(
                        tag_id=tag_id_final,
                        defaults={
                            'ubicacion': row['ubicacion'],
                            'marca': row['marca'],
                            'refrigerante': row['refrigerante'],
                            'voltaje': row['voltaje'],
                            'btu': int(limpiar_num(row['btu'])),
                            'amperaje': limpiar_num(row['amperaje']),
                            'potencia_va': limpiar_num(row['potencia_va']),
                            'potencia_w': limpiar_num(row['potencia_w']),
                        }
                    )
                    count += 1
            
            self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se han cargado {count} equipos al inventario.'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: No se encontró el archivo "{ruta}"'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Error: No se encontró la columna {e}. Revisa el encabezado del CSV.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocurrió un error inesperado: {e}'))