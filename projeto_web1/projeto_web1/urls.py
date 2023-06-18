from django.contrib import admin
from django.urls import include, path
from .views import home_page
from django.views.generic import TemplateView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('cardapio/', include('produtos.urls')),
    path('pedido/', include('pedidos.urls')),
    path('funcionarios/', include('funcionarios.urls')),
<<<<<<< HEAD
    
  
    
   


    
    
   
    
=======
>>>>>>> 28708b05a77014a5fa4f4afb637cbffbda9367d4
]
