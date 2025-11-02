from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout

from .serializers import (
    UsuarioSerializer,
    RegistroUsuarioSerializer,
    LoginSerializer
)
from .models import Usuario
from .permissions import IsAdminWithValidToken


class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [IsAdminWithValidToken]  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Datos inválidos',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()

            return Response({
                'message': 'Usuario creado exitosamente',
                'user': UsuarioSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Error al crear usuario',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUsuarioView(APIView):
    permission_classes = [AllowAny] 
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response({
                'error': 'Credenciales inválidas',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Login exitoso',
            'user': UsuarioSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)


class LogoutUsuarioView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            mensaje = f'Logout exitoso para {request.user.correo}'
            
        except Token.DoesNotExist:
            mensaje = 'No había token activo'

        except Exception as e:
            return Response({
                'error': 'Error al cerrar sesión',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': mensaje,
            'info': 'Tu token ha sido invalidado. Debes iniciar sesión nuevamente para obtener uno nuevo.'
        }, status=status.HTTP_200_OK)


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        campos_bloqueados = ['is_superuser']
        
        for campo in campos_bloqueados:
            if campo in request.data:
                return Response({
                    'error': f'No puedes modificar el campo: {campo}'
                }, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)


class ListarUsuariosView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminWithValidToken]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        is_active = self.request.query_params.get('activo', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.order_by('-fecha_registro')


class DesactivarUsuarioView(APIView):
    permission_classes = [IsAdminWithValidToken]
    
    def patch(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
            
            usuario.is_active = not usuario.is_active
            usuario.save()
            
            return Response({
                'message': f'Usuario {"activado" if usuario.is_active else "desactivado"} exitosamente',
                'user': UsuarioSerializer(usuario).data
            }, status=status.HTTP_200_OK)
            
        except Usuario.DoesNotExist:
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)