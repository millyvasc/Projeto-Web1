from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('funcionarios/', include('funcionarios.urls')),
    path('pedidos/', include('pedidos.urls')),
    

    # --------------- CAMILLE -----------------
    path('<int:mesa>/cardapio/', include('produtos.urls')),
    path('produtos/', include('produtos.urls')),
    
    # --------------Joao V Nascimento ---------------
    path('garcom/', include('garcons.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
