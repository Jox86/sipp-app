from rest_framework import serializers
from apps.reports_app.models import Report, ActaConformidad
from apps.orders.models import Order

class OrderReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullName', read_only=True)
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'project', 'project_name',
            'order_type', 'status', 'items', 'total',
            'completed_at', 'created_at', 'updated_at'
        ]

    def get_project_name(self, obj):
        if obj.project:
            return f'{obj.project.costCenter} - {obj.project.projectNumber}'
        return 'Pedido Extra'

class ReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.fullName', read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
            'generated_by': {'required': False, 'allow_null': True}
        }

class ActaConformidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActaConformidad
        fields = '__all__'