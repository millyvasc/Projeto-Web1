import re
from django import forms
from django.forms import ModelForm
from produtos.models import Produto
from django import forms
from django.db import models


class ProdutoForm(forms.ModelForm):
    required_css_class = 'required'
    tipo = forms.ChoiceField(
        choices=[('prato', 'Prato'), ('bebida', 'Bebida')])
    img = forms.ImageField()

    class Meta:
        model = Produto
        fields = ['cod', 'nome', 'valorUnitario',
                  'descricao', 'estoque', 'tipo', 'img']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'custom-select'}),
        }
        labels = {
            'nome': 'Nome',
            'valorUnitario': 'Valor Unitário',
            'descricao': 'Descrição',
            'estoque': 'Estoque',
            'tipo': 'Tipo',
            'img': 'Imagem',
        }

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
