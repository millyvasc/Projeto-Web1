from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomerUserForm(UserCreationForm):
    
    cpf = forms.CharField(max_length=14)
    telefone = forms.CharField(max_length=16)
    endereco = forms.CharField(max_length=200)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'username', 'email', 'groups', 'cpf', 'telefone', 'endereco']
        
    def save(self, commit=True):
            user = super().save(commit=False)
            if commit:
                user.save()
                self.save_m2m()
                groups = self.cleaned_data.get('groups')  # Obtém os grupos selecionados
                if groups:
                    user.groups.set(groups)  # Associa os grupos selecionados ao usuário
            return user