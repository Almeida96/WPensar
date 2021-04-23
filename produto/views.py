from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView
from .models import Produto

class ProdutoCreateView(CreateView):
    model = Produto
    fields = ['nome']
    success_url = '/adicionar-produto/'

    def post(self, request, *args, **kwargs):
        nome_requisicao = self.request.POST['nome']
         
        try:
            tem_nome_repetido = Produto.objects.get(nome=nome_requisicao)

            if tem_nome_repetido:
                raise ValidationError('O produto já foi cadastrado', code='invalid')

            return super(ProdutoCreateView, self).post(request)
        except Produto.DoesNotExist:
            return super(ProdutoCreateView, self).post(request)