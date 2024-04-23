from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):

    CHOICES_TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('funcionario', 'Funcionario')
    )

    tipo_usuario = models.CharField(
        verbose_name='Tipo de Usuário',
        max_length=100,
        default="cliente",
        choices=CHOICES_TIPO_USUARIO,
    )

    usuario = models.OneToOneField(
        User, 
        verbose_name=("usuario"),   
        on_delete=models.CASCADE,
        null=True
    )

    nome = models.CharField(
        max_length=100, 
        default="NomeUsuário"
    )
    
    data_nascimento = models.DateField(
        null=False,
        blank=False
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=False,
        blank=False
    )

    celular = models.CharField(
        max_length=15,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.usuario.username