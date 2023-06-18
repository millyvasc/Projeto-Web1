from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
<<<<<<< HEAD
=======
    path("<int:produto_cod>/", views.verProduto, name="detalhes"),
    path("pratos/", views.listPratos, name="listar_pratos"),
    path("bebidas/", views.listBebidas, name="listar_bebidas"),
>>>>>>> 28708b05a77014a5fa4f4afb637cbffbda9367d4
]
