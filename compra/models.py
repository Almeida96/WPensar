from django.core.validators import MinValueValidator
from django.db import models
from produto.models import Produto


class Compra(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.PROTECT, verbose_name="Product"
    )
    quantidade = models.PositiveIntegerField(
        "Quantity", validators=[MinValueValidator(1)]
    )
    preco = models.DecimalField(
        "Unit price", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade__gte=1), name="positive_quantity"
            ),
            models.CheckConstraint(
                condition=models.Q(preco__gte=0), name="nonnegative_price"
            ),
        ]

    def __str__(self):
        return f"{self.produto} / {self.quantidade} × {self.preco}"
