from rest_framework import viewsets
from loja.models import Produto
from loja.api.serializers.produto_serializer import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
