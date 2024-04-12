from http import HTTPStatus

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from .models import Client, Appointment
from .serializers import ClientSerializer, AppointmentSerializer


class ClientViewSet(GenericViewSet, CreateModelMixin):
    """Эндпоинт для Сделок."""
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_queryset().filter(telegram_id=kwargs["pk"]).first()
        if not instance:
            return Response(status=HTTPStatus.NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AppointmentViewSet(GenericViewSet, ListModelMixin):
    """Эндпоинт для Записей на прием."""
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=HTTPStatus.BAD_REQUEST)
        else:
            serializer.save()
            data = serializer.data
            return Response(data=data, status=HTTPStatus.OK)

    @action(detail=False, methods=("GET",))
    def user_list(self, request, *args, **kwargs) -> Response:
        user_id = request.query_params.get('user_id')
        queryset = self.get_queryset().filter(owner=user_id)
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data=data, status=HTTPStatus.OK)
