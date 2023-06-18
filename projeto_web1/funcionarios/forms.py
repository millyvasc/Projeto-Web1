from django.forms import ModelForm
from funcionarios.models import Funcionario
from django import forms
from django.forms import ModelForm
from produtos.models import Produto
from django import forms

class FuncionarioForm(forms.ModelForm):
    #opte por não utilizar fields = "__all__" 
    #uma vez que o cod não fará parte do form. Defina os campos em uma lista.
    nome = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    
    


