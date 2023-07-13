from django.contrib import admin
from django.urls import path
from comandas import views

urlpatterns = [
    path('vendas/', views.verHistorico, name="verHistorico"),
    path('vendas/all', views.verHistoricoCompleto, name="verHistoricoCompleto"),
    path("<int:id_comanda>/fecharConta/", views.fecharConta, name="fecharComanda"),
    path("comandas/<int:cod_comanda>/", views.detalharComanda, name="detalharComanda"),
    path("comandas/", views.pedidosFechamento, name="pedidosFechamento"),
    path("comandas/concluir/<int:cod_comanda>/", views.pedidosFechamentoConcluir, name="pedidosFechamentoConcluir"),

#     path("<int:mesa1>/", views.verConta, name="verConta"),
    path("", views.verConta, name="verConta"),
]
