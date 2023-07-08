from django.contrib import admin
from django.urls import include, path
from comandas import views

urlpatterns = [
    path('vendas/', views.verHistorico, name="verHistorico"),
    path('vendas/all', views.verHistoricoCompletp, name="verHistorico"),
    path("<int:mesa1>/", views.verConta, name="verConta"),
    path("<int:id_comanda>/fecharConta/",
         views.fecharConta, name="fecharComanda"),

    path("comandas/<int:cod_comanda>/",
         views.detalharComanda, name="detalharComanda"),


]
