from django.db import models
from django.db.models.functions import Lower


class Produto(models.Model):
    nome = models.CharField("Product name", max_length=100)

    class Meta:
        ordering = ["nome", "id"]
        constraints = [
            models.UniqueConstraint(Lower("nome"), name="unique_product_name")
        ]

    def __str__(self):
        return self.nome
