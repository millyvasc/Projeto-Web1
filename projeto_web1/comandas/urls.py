from django.contrib import admin
from django.urls import include, path
from comandas import views

urlpatterns = [
    path('vendas/', views.verHistorico, name="verHistorico"),
]