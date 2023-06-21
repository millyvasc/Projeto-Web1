import re
from django import forms
from django.forms import ModelForm
from produtos.models import Produto
from django import forms


class ProdutoForm(ModelForm):
    tipo = forms.ChoiceField(
        choices=[('prato', 'Prato'), ('bebida', 'Bebida')])

    class Meta:
        model = Produto
        fields = ['cod', 'nome', 'valorUnitario',
                  'descricao', 'estoque', 'tipo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'custom-select'}),
        }
        labels = {
            'nome': 'Nome',
            'valorUnitario': 'Valor Unitário',
            'descricao': 'Descrição',
            'estoque': 'Estoque',
            'tipo': 'Tipo',
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


class ProdutoPhotoForm(forms.ModelForm):
    required_css_class = 'required'
    # photo = forms.ImageField(required=False)  # Uma foto so
    photo = forms.ImageField(  # VARIAS FOTOS
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Produto
        fields = ('cod', 'nome', 'valorUnitario',
                  'descricao', 'estoque', 'tipo', 'photo')

    def __init__(self, *args, **kwargs):
        super(ProdutoPhotoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = None
