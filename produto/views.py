from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.views.generic.edit import CreateView

from .forms import ProdutoForm
from .models import Produto


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    success_url = "/adicionar-produto/"

    def form_valid(self, form):
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            form.add_error("nome", "This product already exists.")
            return self.form_invalid(form)
