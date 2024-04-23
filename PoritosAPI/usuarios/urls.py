from django.urls import path, include
from rest_framework.routers import DefaultRouter

from usuarios.api.viewsets.usuario_viewset import UsuarioViewSet, user_registration, user_login, teste

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    # ... outras rotas da sua aplicação ...
    path('', include(router.urls)),
    path('register/', user_registration, name='user-registration'),
    path('login/', user_login, name='user-login'),
    path('teste/', teste, name='teste'),

]
