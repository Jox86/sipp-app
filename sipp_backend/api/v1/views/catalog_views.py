from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.catalog.models import Empresa, Producto, Servicio, PedidoExtra
from api.v1.serializers.catalog_serializers import (
    EmpresaSerializer, ProductoSerializer, ServicioSerializer, PedidoExtraSerializer
)


class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'encargado']
    queryset = Empresa.objects.prefetch_related('productos', 'servicios').all()


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['empresa', 'categoria']
    search_fields = ['nombre']
    queryset = Producto.objects.select_related('empresa').all()


class ServicioViewSet(viewsets.ModelViewSet):
    serializer_class = ServicioSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['empresa']
    search_fields = ['nombre']
    queryset = Servicio.objects.select_related('empresa').all()


class PedidoExtraViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoExtraSerializer
    permission_classes = [AllowAny]
    queryset = PedidoExtra.objects.select_related('usuario', 'proyecto').all()
