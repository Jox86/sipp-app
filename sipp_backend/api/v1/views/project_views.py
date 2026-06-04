from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.projects.models import Project, BudgetHistory
from api.v1.serializers.project_serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectCreateUpdateSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user = self.request.user
        # Si está autenticado y es jefe de proyecto, filtrar por owner
        if user.is_authenticated and user.role == 'user':
            return Project.objects.select_related('owner').filter(owner=user)
        # Admin o no autenticado ve todos
        return Project.objects.select_related('owner').all()
        
    def get_queryset(self):
        return Project.objects.select_related('owner').all()

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)