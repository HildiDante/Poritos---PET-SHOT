from django.db import models

class Servico(models.Model):
    TIPO_CHOICES = (
        ('banho', 'Banho'),
        ('tosa', 'Tosa'),
        ('consulta', 'Consulta'),
        ('outro', 'Outro')
    )

    nome = models.CharField(
        max_length=100
    )

    tipo_servico = models.CharField(
        max_length=100,
        choices=TIPO_CHOICES
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tempo_estimado = models.DurationField()

    descontos = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return self.nome
