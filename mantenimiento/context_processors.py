from django.utils import timezone
from datetime import timedelta
from .models import PlanPreventivo

def estadisticas_mantenimiento(request):
    # Solo ejecutamos esto si estamos en el área de administración
    if request.path.startswith('/admin/'):
        hoy = timezone.now().date()
        fecha_limite = hoy + timedelta(days=7)

        vencidos = PlanPreventivo.objects.filter(fecha_proximo_mantenimiento__lt=hoy).count()
        por_vencer = PlanPreventivo.objects.filter(fecha_proximo_mantenimiento__range=[hoy, fecha_limite]).count()
        al_dia = PlanPreventivo.objects.filter(fecha_proximo_mantenimiento__gt=fecha_limite).count()

        return {
            'stats_vencidos': vencidos,
            'stats_por_vencer': por_vencer,
            'stats_al_dia': al_dia,
        }
    return {}