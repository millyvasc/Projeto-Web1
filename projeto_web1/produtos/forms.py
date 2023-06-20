import re
from django import forms  # adicionei
from django.forms import ModelForm
from produtos.models import Produto
from django import forms


class ProdutoForm(ModelForm):
    # opte por não utilizar fields = "__all__"
    # uma vez que o cod não fará parte do form. Defina os campos em uma lista.
    # nome = forms.CharField(widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # estoque = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control"}))

    # ------------------------------------------------------
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Produto
        # fields = '__all__'
        fields = {'cod', 'nome', 'valorUnitario',
                  'descricao', 'estoque', 'tipo'}

    def save(self):
        produto = Produto.objects.create(
            nome=self.cleaned_data["nome"],
            valorUnitario=self.cleaned_data["valorUnitario"],
            descricao=self.cleaned_data["descricao"],
            estoque=self.cleaned_data["estoque"],
            tipo=self.cleaned_data["tipo"]
        )
        return True
