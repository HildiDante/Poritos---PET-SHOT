from os import path
from rest_framework.routers import DefaultRouter

from animal.api.viewset.animal_viewset import AnimalViewSet
from animal.api.viewset.reserva_viewset import ReservaViewSet
from animal.api.viewset.servico_viewset import ServicoViewSet

router = DefaultRouter()
router.register(r'animais', AnimalViewSet, basename='animal')
router.register(r'servicos', ServicoViewSet, basename='servico')
router.register(r'reservas', ReservaViewSet, basename='reserva')
urlpatterns = router.urls

router.register(r'listar_animais_usuario', AnimalViewSet, basename='listar_animais_usuario')
router.register(r'criar_reserva', ReservaViewSet, basename='criar_reserva')