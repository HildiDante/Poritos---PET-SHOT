from django.db import models
from .produto import Produto

class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produto.nome}'

    def save(self, *args, **kwargs):
        self.valor = self.produto.preco * self.quantidade
        super().save(*args, **kwargs)
