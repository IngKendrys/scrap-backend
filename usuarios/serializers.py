from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'nombre_negocio',
            'correo',
            'telefono',
            'direccion',
            'fecha_registro',
            'is_active',
            'is_superuser'
        ]
        read_only_fields = ['id', 'fecha_registro']

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'nombre_negocio',
            'correo',
            'password',
            'telefono',
            'direccion'
        ]

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            nombre_negocio=validated_data['nombre_negocio'],
            correo=validated_data['correo'],
            password=validated_data['password'],
            telefono=validated_data['telefono'],
            direccion=validated_data['direccion']
        )
        return usuario

class ActualizarUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'nombre_negocio',
            'telefono',
            'direccion',
            'correo'
        ]
    
class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        correo = attrs.get('correo')
        password = attrs.get('password')
        
        usuario = Usuario.objects.get(correo=correo)
        
        if not usuario.check_password(password):
            raise serializers.ValidationError(
                'Credenciales incorrectas',
                code='authorization'
            )
        

        if not usuario.is_active:
            raise serializers.ValidationError(
                'Esta cuenta está desactivada',
                code='authorization'
            )
        
        attrs['user'] = usuario
        return attrs