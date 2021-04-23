from django.db import models
from produto.models import Produto

# Create your models here.
class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=True)
    preco = models.FloatField(null=True)

    def __str__(self):
        return f'{self.produto} / {self.quantidade}x / {self.preco}'