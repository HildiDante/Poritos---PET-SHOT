from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from django.utils import timezone
import re

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import action

from usuarios.document.login_schema import request_body_login_schema, login_responses
from drf_yasg.utils import swagger_auto_schema

from usuarios.api.serielizers.usuario_serializer import UsuarioSerializer
from usuarios.models import Usuario

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    http_method_names = ['get', ]

    @action(detail=True, methods=['get'])
    def obter_celular_username(self, request, pk=None):
        try:
            usuario = self.get_object()
            data = {
                'username': usuario.usuario.username,
                'celular': usuario.celular
            }
            return Response(data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=False, methods=['get'])
    def obter_info_por_token(self, request):
        user = request.user
        usuario = Usuario.objects.get(usuario=user)

        response_data = {
            "id": usuario.id,
            "tipo_usuario": usuario.tipo_usuario,
            "nome": usuario.nome,
            "data_nascimento": usuario.data_nascimento,
            "cpf": usuario.cpf,
            "celular": usuario.celular,
            "usuario": user.username 
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        username = request.data.get('email')
        nome = request.data.get('nome')
        password = request.data.get('password')
        tipo = request.data.get('tipo_usuario')
        data_nascimento = request.data.get('data_nascimento')
        cpf = request.data.get('cpf')
        celular = request.data.get('celular')
        celular_formatado = formatar_celular(celular)

        if not (username and password):
            return Response({'error': 'Informe um Email de usuário e senha.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if tipo not in dict(Usuario.CHOICES_TIPO_USUARIO):
            return Response({'error': 'Tipo de usuario inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        data_atual = timezone.now().date()

        if not(nome) or nome == "":
            return Response({'error': 'Informe um nome de usuário.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data_nascimento = timezone.datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Data de nascimento inválida.'}, status=status.HTTP_400_BAD_REQUEST)

        idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

        if idade < 18:
            return Response({'error': 'O usuário deve ter no mínimo 18 anos de idade.'}, status=status.HTTP_400_BAD_REQUEST)

        
        if not verifica_cpf(cpf):
             return Response({'error': 'CPF inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not re.match(r'^\(\d{2}\) \d \d{4}-\d{4}$', celular_formatado):
            return Response({'error': f'Número de celular inválido. Use o formato (xx) x xxxx-xxxx.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validar_email(username):
            return Response({'error': 'Endereço de e-mail inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        
        usuario = Usuario.objects.create(
            tipo_usuario=tipo, 
            nome=nome,
            usuario=user,
            data_nascimento=data_nascimento,
            cpf=cpf,
            celular=celular_formatado,
        )

        usuario_serializer = UsuarioSerializer(usuario)
        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='post',
    request_body=request_body_login_schema,
    responses=login_responses
)
@api_view(['POST'])
def user_login(request):
    username = request.data.get('email')
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
    cpf = request.data.get('cpf')

    print(verifica_cpf(cpf))

    if not isinstance(user, AnonymousUser):
        try:
            usuario = Usuario.objects.get(usuario=user)
        
            user_serializer = UsuarioSerializer(usuario)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Jogador não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

def verifica_cpf(cpf):
    # Remove pontos e traços do CPF e verifica se possui 11 dígitos
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0]*11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # Verifica se os dígitos calculados são iguais aos dígitos fornecidos
    return cpf[-2:] == str(digito1) + str(digito2)

def formatar_celular(numero):
    if re.match(r'^\d{11}$', numero):
        return f'({numero[:2]}) {numero[2]} {numero[3:7]}-{numero[7:]}'
    return numero

def validar_email(email):
    # Padrão da expressão regular para validar e-mails
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(padrao_email, email):
        return True
    return False