from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome"]

    def clean_nome(self):
        name = " ".join(self.cleaned_data["nome"].split())
        if not name:
            raise forms.ValidationError("Enter a product name.")
        if Produto.objects.filter(nome__iexact=name).exists():
            raise forms.ValidationError("This product already exists.")
        return name
