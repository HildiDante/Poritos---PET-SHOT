from rest_framework import viewsets
from loja.models import Compra
from loja.api.serializers.compra_serializer import CompraSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
