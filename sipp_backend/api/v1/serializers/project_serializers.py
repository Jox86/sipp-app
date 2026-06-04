from rest_framework import serializers
from apps.projects.models import Project, BudgetHistory


class BudgetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetHistory
        fields = ['id', 'budget', 'period', 'periodEnd', 'syncedAt']


class ProjectListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.fullName', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'costCenter', 'projectNumber', 'budget',
            'area', 'areaType', 'status', 'endDate', 'renewalDate',
            'budgetPeriod', 'owner', 'owner_name', 'owner_email',
            'created_at', 'updated_at'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.fullName', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    budget_history = BudgetHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'costCenter', 'projectNumber',
            'budget', 'area', 'areaType', 'status', 'endDate',
            'renewalDate', 'budgetPeriod', 'owner'
        ]
