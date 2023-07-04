from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('funcionarios/', include('funcionarios.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('comandas/', include('comandas.urls')),


    # --------------- CAMILLE -----------------
    path('<int:mesa>/cardapio/', include('produtos.urls')),
    path('produtos/', include('produtos.urls')),
    path('painel/', include('funcionarios.urls')),
    path('vendas/', include('comandas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
