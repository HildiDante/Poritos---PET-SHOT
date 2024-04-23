from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import make_naive

from animal.api.serializers.reserva_serializer import ReservaSerializer
from animal.models.animal import Animal
from animal.models.reserva import Reserva
from animal.models.servico import Servico
from usuarios.models.usuario import Usuario

import os

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    @action(detail=False, methods=['post'])
    def criar_reserva(self, request):
        lista_servicos = request.data.get('lista_servicos')
        data = request.data.get('data')
        horario = request.data.get('horario')
        lista_servicos_val = Servico.objects.filter(id__in=lista_servicos)

        data_hora = datetime.strptime(f'{data} {horario}', '%Y-%m-%d %H:%M')

        try:
            animal = Animal.objects.get(id=request.data.get('animal'))
        except Animal.DoesNotExist:
            return Response({'mensagem': 'Animal não encontrado'}, status=status.HTTP_400_BAD_REQUEST)    

        if not isinstance(lista_servicos, list):
            return Response({'mensagem': 'A lista de serviços é inválida'}, status=status.HTTP_400_BAD_REQUEST)


        valor_total = sum(servico.valor for servico in lista_servicos_val)
        tempo_total = sum((servico.tempo_estimado for servico in lista_servicos_val), timedelta())

        horario_final = data_hora + tempo_total

        HORARIO_MANHA_INICIO = datetime.strptime(os.getenv('HORARIO_MANHA_INICIO'), '%H:%M').time()
        HORARIO_MANHA_FIM = datetime.strptime(os.getenv('HORARIO_MANHA_FIM'), '%H:%M').time()
        HORARIO_TARDE_INICIO = datetime.strptime(os.getenv('HORARIO_TARDE_INICIO'), '%H:%M').time()
        HORARIO_TARDE_FIM = datetime.strptime(os.getenv('HORARIO_TARDE_FIM'), '%H:%M').time()

        if not (HORARIO_MANHA_INICIO <= data_hora.time() <= HORARIO_MANHA_FIM) and \
                not (HORARIO_TARDE_INICIO <= horario_final.time() <= HORARIO_TARDE_FIM):
            return Response({'mensagem': 'Horário inválido'}, status=status.HTTP_400_BAD_REQUEST)
              
        if  (HORARIO_MANHA_FIM <= data_hora.time() <= HORARIO_TARDE_INICIO):
            return Response({'mensagem': 'Horário inválido'}, status=status.HTTP_400_BAD_REQUEST)

        if (HORARIO_MANHA_FIM > data_hora.time() and \
                (HORARIO_MANHA_FIM < horario_final.time())):
            horario_final += timedelta(hours=1)

        if Reserva.objects.filter(inicio__lt=horario_final, fim__gt=data_hora).exists():
            return Response({'mensagem': 'Já existe uma reserva para este horário'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(usuario=request.user)
        except Usuario.DoesNotExist:
            return Response({'mensagem': 'Usuario não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({'mensagem': 'Informe um Usuario'}, status=status.HTTP_400_BAD_REQUEST)


        try:
            reserva = Reserva.objects.create(
                usuario=usuario,
                tempo_total=tempo_total,
                inicio=data_hora,
                fim=horario_final,
                valor_total=valor_total,
                animal=animal
            )

            reserva.lista_servicos.set(lista_servicos_val)


            return Response({'mensagem': f'Reserva criada com sucesso'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'mensagem': f'Erro ao criar reserva: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


