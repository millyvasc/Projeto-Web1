from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import FuncionariosView


urlpatterns = [
    path('', views.index, name='dashboard'),
    path('funcionarios/', FuncionariosView.as_view(), name='funcionarios'),
]
