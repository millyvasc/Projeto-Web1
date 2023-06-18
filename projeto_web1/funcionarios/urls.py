from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import ProdutosView


urlpatterns = [
    
    path('funcionarios/', views.index, name='index'),
    path('produtos/', ProdutosView.as_view(), name='produtos'),
    path('funcionarios/', TemplateView.as_view(template_name='funcionarios/index.html'), name='funcionarios'),
    
]

