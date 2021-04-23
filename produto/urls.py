from django.urls import path
from .views import ProdutoCreateView

urlpatterns = [
    path("adicionar-produto/", ProdutoCreateView.as_view(), name="adicionar-produto")
]
