from django.forms import ModelForm
from funcionarios.models import Funcionario
from django import forms
from django.forms import ModelForm
from produtos.models import Produto
from django import forms



class FuncionarioForm(ModelForm):
    #opte por não utilizar fields = "__all__" 
    #uma vez que o cod não fará parte do form. Defina os campos em uma lista.
    class Meta:
        model = Funcionario
        fields = ['cpf', 'telefone', 'endereco','user']
    
    


