from django.contrib import admin
from django.urls import include, path
from .views import home_page
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:mesa>/cardapio/', include('produtos.urls')),
    path('funcionarios/', include('funcionarios.urls')),
    path('pedidos/', include('pedidos.urls')),
]
