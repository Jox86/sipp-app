from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from apps.orders.models import Order
from apps.reports_app.models import Report, ActaConformidad
from api.v1.serializers.report_serializers import (
    OrderReportSerializer, ReportSerializer, ActaConformidadSerializer
)


class OrderReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderReportSerializer
    permission_classes = [AllowAny]  # Cambiar a AllowAny

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.select_related('user', 'project').all()
        if user.role == 'admin':
            return Order.objects.select_related('user', 'project').all()
        return Order.objects.select_related('user', 'project').filter(user=user)

    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        order = self.get_object()
        order.status = 'Completado'
        order.completed_at = timezone.now()
        order.save()
        return Response({'status': 'Completado', 'message': 'Pedido marcado como completado'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        orders = self.get_queryset()
        total = orders.count()
        completed = orders.filter(status='Completado').count()
        pending = orders.filter(status__in=['Pendiente', 'En proceso']).count()
        total_amount = orders.aggregate(Sum('total'))['total__sum'] or 0
        return Response({
            'total': total, 'completed': completed, 'pending': pending,
            'total_amount': float(total_amount)
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Report.objects.filter(generated_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


class ActaConformidadViewSet(viewsets.ModelViewSet):
    serializer_class = ActaConformidadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ActaConformidad.objects.all()
        return ActaConformidad.objects.filter(generated_by=user)

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


import datetime
from django.utils import timezone
