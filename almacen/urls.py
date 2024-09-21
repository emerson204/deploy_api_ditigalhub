from django.urls import path
from .views import * 

urlpatterns = [
  # Urls de categorias
  path("categorias/list/", CategoriasListView.as_view()),
  path("categorias/create/", CategoriasCreateView.as_view()),
  path("categorias/update/<int:pk>/", CategoriasUpdateView.as_view()),
  path("categorias/delete/<int:pk>/", CategoriasDeleteView.as_view()),
  
  # Urls de productos
  path("productos/list/", ProductosListView.as_view()),
  path("productos/create/", ProductosCreateView.as_view()),
  path("productos/update/<int:pk>/", ProductosUpdateView.as_view()),
  path("productos/delete/<int:pk>/", ProductosDeleteView.as_view()),
  
  # Urls de direcciones
  path("direcciones/list/", DireccionesListView.as_view()),
  path("direcciones/create/", DireccionesCreateView.as_view()),
  path("direcciones/update/<int:pk>/", DireccionesUpdateView.as_view()),
  path("direcciones/delete/<int:pk>/", DireccionesDeleteView.as_view()),
]
    
