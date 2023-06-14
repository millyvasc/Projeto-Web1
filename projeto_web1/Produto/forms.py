from django.forms import ModelForm
from Produto.models import Produtos
from django import forms


class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    estoque = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))