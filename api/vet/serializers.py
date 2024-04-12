from .models import Client, Appointment
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    """Сериалайзер для Клиентов."""

    class Meta:
        model = Client
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    """Сериалайзер для Записей на прием."""

    class Meta:
        model = Appointment
        fields = "__all__"


