from rest_framework import serializers
from apps.conectividad.models import ServicioConectividad

class ServicioConectividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioConectividad
        fields = '__all__'