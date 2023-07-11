from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomerUserForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'username', 'email', 'groups']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
            groups = self.cleaned_data.get('groups')
            if groups:
                user.groups.set(groups)
        return user
