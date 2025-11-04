from django.conf import settings
from django.db import models

ESTADOS_PRODUCTO = [
    ('Nuevo', 'Nuevo'),
    ('Usado', 'Usado'),
]

def validator(value):
    if not value:
        raise ValueError("Este campo no puede estar vacío.")

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=50, 
        unique=True, 
        validators=[validator])
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'CATEGORIAS'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nombre']

    
class Producto(models.Model):
    id_producto = models.AutoField(
        primary_key=True, 
        db_column='id_producto',
        verbose_name='ID Producto'
    )
    nombre = models.CharField(
        max_length=100, 
        validators=[validator],
        db_column='nombre',
        verbose_name='Nombre del Producto'
    )
    descripcion = models.TextField(
        validators=[validator],
        db_column='descripcion',
        verbose_name='Descripción del Producto'
    )
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validator],
        db_column='precio',
        verbose_name='Precio del Producto'
    )
    cantidad = models.IntegerField(
        validators=[validator],
        db_column='cantidad',
        verbose_name='Cantidad del Producto'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vendido = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=20, choices=ESTADOS_PRODUCTO, default='Nuevo',
        db_column='estado',
        verbose_name='Estado del Producto'
    )
    vendido = models.BooleanField(
        default=False,
        db_column='vendido',
        verbose_name='Producto Vendido'
    )
    id_negocio = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='productos',
        db_column='id_negocio',
        verbose_name='ID Negocio', 
    )
    id_categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='id_categoria',
        verbose_name='ID Categoria'
    )
    imagen = models.ImageField(
        upload_to='productos/', blank=True, null=True,
        db_column='imagen',
        verbose_name='Imagen del Producto'
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']


class ImagenProducto(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE, 
        related_name='imagenes'
    )
    
    imagen_url = models.URLField(
        max_length=500,
        db_column='imagen_url',
        verbose_name='URL de la Imagen',
        help_text='URL de Supabase Storage'
    )

    def __str__(self):
        return f"Imagen de {self.id_producto.nombre}"
    
    class Meta:
        db_table = 'IMAGENES_PRODUCTOS'
        verbose_name = 'Imagen Producto'
        verbose_name_plural = 'Imagenes Productos'
        ordering = ['id_producto']