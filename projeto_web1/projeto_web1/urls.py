from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('funcionarios/', include('funcionarios.urls')),
    path('pedidos/', include('pedidos.urls')),


    # --------------- CAMILLE -----------------
    path('<int:mesa>/cardapio/', include('produtos.urls')),
    path('produtos/', include('produtos.urls')),
]