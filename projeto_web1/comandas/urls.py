from django.contrib import admin
from django.urls import include, path
from comandas import views

urlpatterns = [
    path('vendas/', views.verHistorico, name="verHistorico"),
    path('vendas/all', views.verHistoricoCompleto, name="verHistoricoCompleto"),
    path("<int:mesa1>/", views.verConta, name="verConta"),
    path("<int:id_comanda>/fecharConta/", views.fecharConta, name="fecharComanda"),
    path("comandas/<int:cod_comanda>/", views.detalharComanda, name="detalharComanda"),
    path("comandas/", views.pedidosFechamento, name="pedidosFechamento"),
    path("comandas/concluir/<int:cod_comanda>/", views.pedidosFechamentoConcluir, name="pedidosFechamentoConcluir"),

]
