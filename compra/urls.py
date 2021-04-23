from django.urls import path
from .views import CompraCreateView, compras

urlpatterns = [
    path("adicionar-compra/", CompraCreateView.as_view(), name="adicionar-compra"),
    path("", compras, name="compras"),
]
