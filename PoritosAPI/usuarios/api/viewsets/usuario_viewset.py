from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser



from usuarios.api.serielizers.usuario_serializer import UsuarioSerializer
from usuarios.models import Usuario

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    http_method_names = ['get', ]

@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        tipo = request.data.get('tipo_usuario')

        if not (username and password):
            return Response({'error': 'Informe um nome de usuário e senha.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if tipo not in dict(Usuario.CHOICES_TIPO_USUARIO):
            return Response({'error': 'Tipo de usuario inválido'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        usuario = Usuario.objects.create(nome_completo=request.data.get('nome_completo'),tipo_usuario=tipo, usuario=user)

        usuario_serializer = UsuarioSerializer(usuario)
        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    else:
        return Response({'error': 'Credenciais inválidas'}, status=401)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def teste(request):
    user = request.user

    if not isinstance(user, AnonymousUser):
        try:
            usuario = Usuario.objects.get(usuario=user)
        
            user_serializer = UsuarioSerializer(usuario)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Jogador não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)