from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic.edit import CreateView
from produto.models import Produto

from .models import Compra


class CompraCreateView(LoginRequiredMixin, CreateView):
    model = Compra
    fields = ["produto", "quantidade", "preco"]
    success_url = "/compras/"


def purchase_summary():
    products = (
        Produto.objects.filter(compra__isnull=False)
        .distinct()
        .prefetch_related(
            Prefetch("compra_set", queryset=Compra.objects.order_by("id"))
        )
    )
    result = []
    for product in products:
        purchases = list(product.compra_set.all())
        quantity = sum(item.quantidade for item in purchases)
        total = sum((item.quantidade * item.preco for item in purchases), Decimal("0"))
        result.append(
            {
                "produto": product.nome,
                "compras": purchases,
                "total_gasto": total,
                "quantidade_total": quantity,
                "valor_medio": total / quantity,
            }
        )
    return result


@login_required
@require_GET
def compras(request):
    return render(
        request, "compra/compras.html", {"lista_compra_detalhe": purchase_summary()}
    )
