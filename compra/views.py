from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
from django.db.models.query import QuerySet
from django.db.models import Sum

from .models import Compra
from produto.models import Produto

class CompraCreateView(CreateView):
    model = Compra
    fields = ['produto', 'quantidade', 'preco']
    success_url = '/adicionar-compra/'

@require_http_methods(["GET"])
def compras(request):
    lista_produtos = Produto.objects.all()

    resultado = []

    for value in lista_produtos:
        compra = Compra.objects.filter(produto=value)

        if compra.count() > 0:
            compra_detalhe = {
                'produto': value.nome,
                'compras': compra,
                'total_gasto': 0,
                'valor_medio': 0,
            }

            for item in compra:
                compra_detalhe['total_gasto'] += item.quantidade * item.preco
                
            quantidade_total = compra.aggregate(Sum('quantidade'))

            compra_detalhe['valor_medio'] = compra_detalhe['total_gasto'] / quantidade_total['quantidade__sum']

            resultado.append(compra_detalhe)

    context = {
        'lista_compra_detalhe': resultado
    }

    return render(request, template_name='compra/compras.html', context=context)
