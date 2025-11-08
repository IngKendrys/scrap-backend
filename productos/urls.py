from django.urls import path
from productos.views import (
    CategoriaListCreateView,
    CategoriaDetailView,
    
    ProductoCreateView,
    ProductoDetailView,
    ProductoUpdateView,
    ProductoDeleteView,
    
    MisProductosListView,

    ImagenProductoCreateView,
    ImagenProductoDeleteView,
)

app_name = 'productos'

urlpatterns = [
    path('categorias/', CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('categorias/<int:id_categoria>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    
    path('crear/', ProductoCreateView.as_view(), name='producto-create'),
    path('<int:id_producto>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('editar/<int:id_producto>/', ProductoUpdateView.as_view(), name='producto-update'),
    path('eliminar/<int:id_producto>/', ProductoDeleteView.as_view(), name='producto-delete'),
    
    path('mis-productos/', MisProductosListView.as_view(), name='mis-productos'),
                    
    path('imagenes/crear/', ImagenProductoCreateView.as_view(), name='imagen-create'),
    path('imagenes/<int:id_imagen>/eliminar/', ImagenProductoDeleteView.as_view(), name='imagen-delete'),
]