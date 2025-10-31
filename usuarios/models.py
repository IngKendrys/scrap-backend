from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

def validator(value):
    if not value or not value.strip():
        raise ValueError('Este campo no puede estar vacío o contener solo espacios en blanco.')
    return value.strip()

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_negocio, usuario, correo, contrasena, telefono, direccion, **extra_fields):    
        correo = self.normalize_email(correo)
        user = self.model(
            nombre_negocio=nombre_negocio,
            usuario=usuario,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            contrasena=contrasena,
            **extra_fields
        )
        user.set_password(contrasena)
        user.save(using=self._db)

        
        return user

    def create_superuser(self, nombre_negocio, usuario, correo, contrasena, telefono, direccion, **extra_fields):
        extra_fields.setdefault('es_superuser', True)
        extra_fields.setdefault('estado', True)


        return self.create_user(nombre_negocio, usuario, correo, contrasena, telefono, direccion, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(
        primary_key=True, 
        db_column='id',
        validators=[validator]
    )

    nombre_negocio = models.CharField(
        max_length=200, 
        unique=True, 
        db_column='nombre_negocio',
        validators=[validator]
    )

    correo = models.EmailField(
        unique=True, 
        db_column='correo',
        validators=[validator]
    )

    contrasena = models.CharField(
        max_length=128,
        db_column='contrasena',
        validators=[validator],         
        default='defaultpassword'
    )

    telefono = models.CharField(
        max_length=10, 
        unique=True, 
        db_column='telefono',
        validators=[validator]
    )

    direccion = models.CharField(
        max_length=255, 
        db_column='direccion',
        validators=[validator]
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True, 
        db_column='fecha_registro'
    )

    usuario = models.CharField(
        max_length=50, 
        unique=True,
        validators=[validator], 
        db_column='usuario'
    )

    estado = models.BooleanField(
        default=False, 
        db_column='estado'
    )


    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'  
    REQUIRED_FIELDS = ['usuario', 'nombre_negocio', 'telefono', 'direccion']

    class Meta:
        db_table = 'USUARIOS' 
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_negocio} ({self.correo})"
