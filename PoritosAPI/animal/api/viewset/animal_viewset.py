from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from animal.api.serializers.animal_serializer import AnimalSerializer
from animal.models.animal import Animal
from usuarios.models.usuario import Usuario

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def create(self, request, *args, **kwargs):

        nome = request.data.get('nome')
        especie = request.data.get('especie')
        raca = request.data.get('raca')
        peso = request.data.get('peso')
        idade = request.data.get('idade')
        sexo = request.data.get('sexo')
        foto = request.data.get('foto')

        if not nome or not especie or not raca or not idade or not sexo:
            return Response({'mensagem': 'Campos obrigatórios não fornecidos'}, status=status.HTTP_400_BAD_REQUEST)

        if especie not in dict(Animal.ESPECIES_CHOICES):
                return Response({'error': 'Espécie inválida'}, status=status.HTTP_400_BAD_REQUEST)
        
        if sexo not in dict(Animal.SEXO_CHOICES):
                return Response({'error': 'Sexo do Animal inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(usuario=request.user)
        except Usuario.DoesNotExist:
            usuario = None

        if peso is None:
            peso = '0.00'

        if foto is None:
            foto = 'imagens/animal_fotos/NoImage.png'
        
        animal = Animal.objects.create(
            usuario=usuario,
            nome=nome,
            especie=especie,
            raca=raca,
            peso=peso,
            idade=idade,
            sexo=sexo,
            foto=foto
        )

        # Serializar a resposta
        serializer = self.get_serializer(animal)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'])
    def listar_animais_usuario(self, request):
        # Obter o usuário associado ao token
        try:
            usuario = Usuario.objects.get(usuario=request.user)
        except Usuario.DoesNotExist:
            usuario = None

        # Obter todos os animais vinculados ao usuário
        animais = Animal.objects.filter(usuario=usuario)

        # Serializar a lista de animais
        serializer = self.get_serializer(animais, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)