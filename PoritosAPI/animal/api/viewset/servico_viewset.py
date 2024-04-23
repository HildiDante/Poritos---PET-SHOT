from rest_framework import viewsets

from animal.api.serializers.servico_serializer import ServicoSerializer
from animal.models.servico import Servico

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
