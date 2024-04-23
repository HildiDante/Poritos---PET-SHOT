from django.urls import include, path
from rest_framework.routers import DefaultRouter
from loja.api.viewset.produto_viewset import ProdutoViewSet
from loja.api.viewset.compra_viewset import CompraViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'compras', CompraViewSet, basename='compra')

urlpatterns = [
    path('', include(router.urls)),
]
