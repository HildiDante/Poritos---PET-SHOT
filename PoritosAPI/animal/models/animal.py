from django.db import models
from usuarios.models.usuario import Usuario

class Animal(models.Model):
    ESPECIES_CHOICES = (
        ('cachorro', 'Cachorro'),
        ('gato', 'Gato'),
        ('outro', 'Outro'),
    )

    SEXO_CHOICES = (
        ('macho', 'Macho'),
        ('femea', 'Fêmea'),
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='animais'
    )

    nome = models.CharField(
        max_length=100
    )
    
    especie = models.CharField(
        max_length=100,
        choices=ESPECIES_CHOICES
    )

    raca = models.CharField(
        max_length=100
    )

    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default='0.00'
    )

    idade = models.PositiveIntegerField()

    sexo = models.CharField(
        max_length=100,
        choices=SEXO_CHOICES
    )

    foto = models.ImageField(
        upload_to='imagens/animal_fotos/',
        null=True,
        blank=True,
        default='imagens/animal_fotos/NoImage.png'
    )

    def __str__(self):
        return self.nome
