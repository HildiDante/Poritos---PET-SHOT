from django.db import models
from animal.models.animal import Animal
from animal.models.servico import Servico
from usuarios.models.usuario import Usuario

class Reserva(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE, 
        related_name='reservas'
    )
    
    lista_servicos = models.ManyToManyField(Servico)
    
    tempo_total = models.DurationField()
    
    inicio = models.DateTimeField()
    
    fim = models.DateTimeField()
    
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'Reserva de {self.usuario} em {self.inicio}'
