from rest_framework import serializers
from productos.models import Categoria, Producto, ImagenProducto
from django.utils import timezone

class CategoriaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Categoria
        fields = ['id_categoria', 'nombre', 'descripcion']
        read_only_fields = ['id_categoria']

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ['id_imagen', 'imagen_url', 'id_producto']
        read_only_fields = ['id_imagen']

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source='id_categoria.nombre',
        read_only=True
    )
    negocio_nombre = serializers.CharField(
        source='id_negocio.nombre_negocio',
        read_only=True
    )
    
    class Meta:
        model = Producto
        fields = [
            'id_producto',
            'nombre',
            'precio',
            'cantidad',
            'estado',
            'vendido',
            'categoria_nombre',
            'negocio_nombre',
            'fecha_creacion'
        ]
        read_only_fields = ['id_producto', 'fecha_creacion']


class ProductoDetailSerializer(ProductoSerializer):
    categoria = CategoriaSerializer(source='id_categoria', read_only=True)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    
    class Meta(ProductoSerializer.Meta):
        fields = ProductoSerializer.Meta.fields + [
            'descripcion',
            'categoria',
            'imagenes',
            'fecha_vendido',
            'imagen'  
        ]


class ProductoCreateSerializer(serializers.ModelSerializer):
    imagenes_urls = serializers.ListField(
        child=serializers.URLField(max_length=500),
        write_only=True,
        required=False,
        help_text="Lista de URLs de imágenes del producto"
    )
    
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'cantidad',
            'estado',
            'id_categoria',
            'imagenes_urls'
        ]
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value
    
    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad debe ser mayor o igual a 0.")
        return value
    
    def create(self, validated_data):
        imagenes_urls = validated_data.pop('imagenes_urls', [])
        
        validated_data['id_negocio'] = self.context['request'].user
        
        producto = Producto.objects.create(**validated_data)
        
        for url in imagenes_urls:
            ImagenProducto.objects.create(
                id_producto=producto,
                imagen_url=url
            )
        
        return producto


class ProductoUpdateSerializer(serializers.ModelSerializer):
    imagenes_urls = serializers.ListField(
        child=serializers.URLField(max_length=500),
        write_only=True,
        required=False,
        help_text="Agregar nuevas URLs de imágenes"
    )
    
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'cantidad',
            'estado',
            'vendido',
            'id_categoria',
            'imagenes_urls'
        ]
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value
    
    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad debe ser mayor o igual a 0.")
        return value
    
    def update(self, instance, validated_data):
        imagenes_urls = validated_data.pop('imagenes_urls', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        for url in imagenes_urls:
            ImagenProducto.objects.create(
                id_producto=instance,
                imagen_url=url
            )
        
        return instance


class MarcarVendidoSerializer(serializers.Serializer):
    vendido = serializers.BooleanField(required=True)
    
    def update(self, instance, validated_data):
        vendido = validated_data.get('vendido')
        
        if vendido:
            instance.vendido = True
            instance.fecha_vendido = timezone.now()
            instance.cantidad = instance.cantidad - 1 if instance.cantidad > 0 else 0
        else:
            instance.vendido = False
            instance.fecha_vendido = None
        
        instance.save()
        return instance