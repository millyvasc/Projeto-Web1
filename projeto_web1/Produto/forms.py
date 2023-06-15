from django.forms import ModelForm
from Produto.models import Produtos
from django import forms


class ProdutoForm(forms.ModelForm):
    #opte por não utilizar fields = "__all__" 
    #uma vez que o cod não fará parte do form. Defina os campos em uma lista.
    nome = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    estoque = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))