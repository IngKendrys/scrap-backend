from rest_framework import status, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from productos.models import Categoria, Producto, ImagenProducto
from productos.serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    ProductoDetailSerializer,
    ProductoCreateSerializer,
    ProductoUpdateSerializer,
    ImagenProductoSerializer
)
from usuarios.permissions import IsAdminWithValidToken

class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminWithValidToken()]
        return [IsAuthenticated()]


class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'id_categoria'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminWithValidToken()]


class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(id_negocio=self.request.user)

class ProductoDetailView(generics.RetrieveAPIView):
    queryset = Producto.objects.select_related('id_categoria', 'id_negocio').prefetch_related('imagenes')
    serializer_class = ProductoDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_producto'


class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_producto'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Producto.objects.all()
        return Producto.objects.filter(id_negocio=user)


class ProductoDeleteView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_producto'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Producto.objects.all()
        return Producto.objects.filter(id_negocio=user)

class MisProductosListView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['fecha_creacion', 'precio', 'nombre']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Producto.objects.filter(id_negocio=user).select_related('id_categoria')
        
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id:
            queryset = queryset.filter(id_categoria=categoria_id)
        
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        
        vendido = self.request.query_params.get('vendido', None)
        if vendido is not None:
            vendido_bool = vendido.lower() == 'true'
            queryset = queryset.filter(vendido=vendido_bool)
        
        return queryset

class ImagenProductoCreateView(generics.CreateAPIView):
    queryset = ImagenProducto.objects.all()
    serializer_class = ImagenProductoSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id_producto = request.data.get('id_producto')
        imagen = request.FILES.get('imagen_url')  

        if not imagen:
            return Response({'error': 'No se envió ninguna imagen'}, status=status.HTTP_400_BAD_REQUEST)

        nueva_imagen = ImagenProducto.objects.create(
            id_producto_id=id_producto,
            imagen_url=imagen  
        )

        serializer = ImagenProductoSerializer(nueva_imagen)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ImagenProductoDeleteView(generics.DestroyAPIView):
    queryset = ImagenProducto.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_imagen'