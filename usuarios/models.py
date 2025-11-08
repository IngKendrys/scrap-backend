from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

def validator(value):
    if not value or not value.strip():
        raise ValueError('Este campo no puede estar vacío o contener solo espacios en blanco.')
    return value.strip()

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_negocio, correo, password, telefono, direccion, **extra_fields):    
        correo = self.normalize_email(correo)
        extra_fields.setdefault('is_active', True)
        user = self.model(
            nombre_negocio=nombre_negocio,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, nombre_negocio, correo, password, telefono, direccion, **extra_fields):
        extra_fields.setdefault('is_superuser', True) 
        extra_fields.setdefault('is_active', True)

        return self.create_user(nombre_negocio, correo, password, telefono, direccion, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(
        primary_key=True, 
        db_column='id', 
        verbose_name='ID'
    )

    nombre_negocio = models.CharField(
        max_length=200, 
        unique=True, 
        db_column='nombre_negocio',
        validators=[validator],
        verbose_name='Nombre del Negocio'
    )

    correo = models.EmailField(
        unique=True, 
        db_column='correo',
        validators=[validator],
        verbose_name='Correo Electrónico'   
    )

    telefono = models.CharField(
        max_length=10, 
        unique=True, 
        db_column='telefono',
        validators=[validator],
        verbose_name='Teléfono'
    )

    direccion = models.CharField(
        max_length=255, 
        db_column='direccion',
        validators=[validator],
        verbose_name='Dirección'
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True, 
        db_column='fecha_registro',
        verbose_name='Fecha de Registro'
    )

    is_active = models.BooleanField(
        default=True,
        db_column='estado',
        verbose_name='Cuenta Activa'
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'  
    REQUIRED_FIELDS = ['nombre_negocio', 'telefono', 'direccion']

    class Meta:
        db_table = 'USUARIOS' 
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_negocio} ({self.correo})"
