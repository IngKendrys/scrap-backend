from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsAdminWithValidToken(permissions.BasePermission):
    message = 'No tienes permisos de administrador o tu token ha expirado.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            self.message = 'Debes estar autenticado para realizar esta acción.'
            return False
        
        if not (request.user.is_superuser):
            self.message = 'No tienes permisos de administrador.'
            return False
        
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if not auth_header.startswith('Token '):
                self.message = 'Token de autenticación inválido.'
                return False
            
            return True
            
        except Token.DoesNotExist:
            self.message = 'Token inválido o sesión cerrada. Por favor, inicia sesión nuevamente.'
            return False
        except Exception as e:
            self.message = f'Error al validar token: {str(e)}'
            return False

