# productos/urls.py

from django.urls import path
from productos.views import (
    # Categorías
    CategoriaListCreateView,
    CategoriaDetailView,
    
    # Productos - CRUD
    ProductoCreateView,
    ProductoDetailView,
    ProductoUpdateView,
    ProductoDeleteView,
    
    # Productos - Listar con filtros
    MisProductosListView,
    ProductosPorCategoriaView,
    ProductosPorEstadoView,
    ProductosVendidosView,
    ProductosDisponiblesView,
    
    # Marcar vendido
    MarcarVendidoView,
    
    # Imágenes
    ImagenProductoCreateView,
    ImagenProductoDeleteView,
)

app_name = 'productos'

urlpatterns = [
    path('categorias/', CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('categorias/<int:id_categoria>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    
    path('crear/', ProductoCreateView.as_view(), name='producto-create'),
    path('<int:id_producto>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('<int:id_producto>/editar/', ProductoUpdateView.as_view(), name='producto-update'),
    path('<int:id_producto>/eliminar/', ProductoDeleteView.as_view(), name='producto-delete'),
    
    path('mis-productos/', MisProductosListView.as_view(), name='mis-productos'),
    
    path('categoria/<int:id_categoria>/', ProductosPorCategoriaView.as_view(), name='productos-por-categoria'),
    
    path('estado/<str:estado>/', ProductosPorEstadoView.as_view(), name='productos-por-estado'),
    
    path('vendidos/', ProductosVendidosView.as_view(), name='productos-vendidos'),
    path('disponibles/', ProductosDisponiblesView.as_view(), name='productos-disponibles'),
    
    path('<int:id_producto>/marcar-vendido/', MarcarVendidoView.as_view(), name='marcar-vendido'),
    
    path('imagenes/crear/', ImagenProductoCreateView.as_view(), name='imagen-create'),
    path('imagenes/<int:id_imagen>/eliminar/', ImagenProductoDeleteView.as_view(), name='imagen-delete'),
]