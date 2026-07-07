from django.utils import timezone
from datetime import timedelta, datetime  # <-- Agregamos datetime aquí
from django.db.models import Count        # <-- Agregamos Count para contar los reportes
from django.db.models.functions import TruncMonth # <-- Agregamos TruncMonth para agrupar por mes
from .models import PlanPreventivo
from reportes.models import ReporteServicio  # <-- Importamos tu modelo de reportes (ajusta el nombre si es distinto)

def estadisticas_mantenimiento(request):
    # Solo ejecutamos esto si estamos en el área de administración
    if request.path.startswith('/admin/'):
        hoy = timezone.now().date()
        fecha_limite = hoy + timedelta(days=7)

        # Tu lógica actual de filtrado (se mantiene igual)
        vencidos = PlanPreventivo.objects.filter(fecha_proximo_mantenimiento__lt=hoy).count()
        por_vencer = PlanPreventivo.objects.filter(fecha_proximo_mantenimiento__range=[hoy, fecha_limite]).count()
        al_dia = PlanPreventivo.objects.filter(fecha_proximo_mantenimiento__gt=fecha_limite).count()

        # ==========================================
        # NUEVO: Lógica para el gráfico de barras
        # ==========================================
        año_actual = datetime.now().year
        historico_reportes = (
            ReporteServicio.objects.filter(fecha_ejecucion__year=año_actual)
            .annotate(mes=TruncMonth('fecha_ejecucion'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )

        datos_por_mes = [0] * 12
        for registro in historico_reportes:
            if registro['mes']:
                numero_mes = registro['mes'].month
                datos_por_mes[numero_mes - 1] = registro['total']
        # ==========================================

        return {
            'stats_vencidos': vencidos,
            'stats_por_vencer': por_vencer,
            'stats_al_dia': al_dia,
            'datos_barras': datos_por_mes,  # <-- Enviamos la nueva variable al HTML
        }
        
    return {}