from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nome_completo = models.CharField(
        verbose_name='Nome Completo',
        max_length=100,
        null=False
    )

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
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.nome_completo