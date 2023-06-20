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

    def save(self, commit=True):
        produto = super().save(commit=False)
        if not self.instance:  # Verificar se é criação de produto
            produto.nome = self.cleaned_data["nome"]
            produto.valorUnitario = self.cleaned_data["valorUnitario"]
            produto.descricao = self.cleaned_data["descricao"]
            produto.estoque = self.cleaned_data["estoque"]
            produto.tipo = self.cleaned_data["tipo"]
        if commit:
            produto.save()
        return produto
