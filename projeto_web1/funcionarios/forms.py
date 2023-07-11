from django.forms import ModelForm
from funcionarios.models import Funcionario
from django import forms
from django.forms import ModelForm
from produtos.models import Produto
from django import forms

class FuncionarioForm(ModelForm):

    class Meta:
        model = Funcionario
        fields = ['cpf', 'telefone', 'endereco']
        labels = {
            'cpf': 'CPF',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
            
        }
