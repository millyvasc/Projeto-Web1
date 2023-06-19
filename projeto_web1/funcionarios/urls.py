from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import ProdutosView
from .views import FuncionariosView


urlpatterns = [
    
    path('', views.index, name='index'),
    path('produtos/', ProdutosView.as_view(), name='produtos'),
    path('funcionarios/', FuncionariosView.as_view(), name='funcionarios'),
   
    
    
]

