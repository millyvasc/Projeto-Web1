from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomerUserForm(UserCreationForm):
    required_css_class = 'required'

    cpf = forms.CharField(max_length=14)
    telefone = forms.CharField(max_length=16)
    endereco = forms.CharField(max_length=200)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'username', 'email',
                  'groups', 'cpf', 'telefone', 'endereco']
        labels = {
            'first_name': 'Primeiro Nome',
            'username': 'Usuário',
            'email': 'Email',
            'groups': 'Grupos',
            'cpf': 'CPF',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
            # Obtém os grupos selecionados
            groups = self.cleaned_data.get('groups')
            if groups:
                # Associa os grupos selecionados ao usuário
                user.groups.set(groups)
        return user
