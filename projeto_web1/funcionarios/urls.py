from django.urls import path
from . import views
from .views import FuncionariosView

urlpatterns = [
    path("register", views.register, name="register"),
    path('', views.index2, name='index'),
    path("edit/<int:funcionarios_id>/", views.edit, name="edit"),
    path('acesso-negado/', views.acesso_negado, name='acesso_negado'),
    path("remove/<int:funcionarios_id>/", views.remove, name="remove"),
    path("remove/final/<int:funcionarios_id>/",views.removeFinal, name="removeFinal"),
    path('', views.index2, name='dashboard'),
    path('funcionarios/', FuncionariosView.as_view(), name='funcionarios'),
    # ------------------------------------ impressora ---------------------------------------
    path("definir_impressora/", views.definir_impressora_padrao, name="definir_impressora")
]
