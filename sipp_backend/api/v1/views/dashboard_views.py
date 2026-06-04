from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order
from apps.projects.models import Project
from apps.accounts.models import User


class DashboardView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        is_authenticated = user.is_authenticated
        
        # Si no está autenticado, mostrar todos los datos
        if not is_authenticated:
            orders = Order.objects.all()
            projects = Project.objects.all()
            users = User.objects.filter(is_active=True)
        elif user.role == 'admin':
            orders = Order.objects.all()
            projects = Project.objects.all()
            users = User.objects.filter(is_active=True)
        elif user.role == 'user':
            orders = Order.objects.filter(user=user)
            projects = Project.objects.filter(owner=user)
            users = User.objects.filter(id=user.id)
        else:
            orders = Order.objects.filter(user=user)
            projects = Project.objects.none()
            users = User.objects.filter(id=user.id)

        # Estadísticas
        total_pedidos = orders.count()
        pedidos_pendientes = orders.filter(status='Pendiente').count()
        pedidos_completados = orders.filter(status='Completado').count()
        pedidos_en_proceso = orders.filter(status='En proceso').count()
        pedidos_denegados = orders.filter(status='Denegado').count()

        presupuesto_total = projects.aggregate(Sum('budget'))['budget__sum'] or 0
        presupuesto_utilizado = orders.aggregate(Sum('total'))['total__sum'] or 0
        presupuesto_disponible = max(0, float(presupuesto_total) - float(presupuesto_utilizado))

        # Tendencia mensual
        monthly_trends = []
        for i in range(5, -1, -1):
            month_start = (timezone.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1)
            month_orders = orders.filter(created_at__gte=month_start, created_at__lt=month_end)
            monthly_trends.append({
                'month': month_start.strftime('%b %Y'),
                'total_pedidos': month_orders.count(),
                'completados': month_orders.filter(status='Completado').count(),
                'pendientes': month_orders.filter(status='Pendiente').count(),
                'monto_total': float(month_orders.aggregate(Sum('total'))['total__sum'] or 0),
            })

        # Proyectos top
        top_projects = []
        for p in projects.annotate(pedidos_count=Count('orders'), gastado_sum=Sum('orders__total')).filter(pedidos_count__gt=0).order_by('-pedidos_count')[:6]:
            gastado = float(p.gastado_sum or 0)
            presupuesto = float(p.budget or 0)
            top_projects.append({
                'id': p.id,
                'nombre': f'{p.costCenter} - {p.projectNumber}',
                'pedidos': p.pedidos_count,
                'presupuesto': presupuesto,
                'gastado': gastado,
                'porcentaje': min((gastado / presupuesto * 100) if presupuesto > 0 else 0, 100),
            })

        # Pedidos recientes
        recent_orders = []
        for o in orders.select_related('user', 'project').order_by('-created_at')[:6]:
            recent_orders.append({
                'id': o.id,
                'user_name': o.user.fullName if o.user else 'N/A',
                'project_name': f'{o.project.costCenter} - {o.project.projectNumber}' if o.project else 'N/A',
                'order_type': o.order_type,
                'status': o.status,
                'total': float(o.total),
                'created_at': o.created_at.isoformat(),
            })

        return Response({
            'stats': {
                'total_pedidos': total_pedidos,
                'pedidos_pendientes': pedidos_pendientes,
                'pedidos_completados': pedidos_completados,
                'pedidos_en_proceso': pedidos_en_proceso,
                'pedidos_denegados': pedidos_denegados,
                'presupuesto_total': float(presupuesto_total),
                'presupuesto_utilizado': float(presupuesto_utilizado),
                'presupuesto_disponible': presupuesto_disponible,
                'usuarios_activos': orders.values('user').distinct().count(),
                'proyectos_activos': orders.exclude(project=None).values('project').distinct().count(),
                'total_usuarios': users.count(),
                'total_proyectos': projects.count(),
            },
            'monthly_trends': monthly_trends,
            'top_projects': top_projects,
            'recent_orders': recent_orders,
        })