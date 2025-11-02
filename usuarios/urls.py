from django.urls import path
from .views import (
    RegistroUsuarioView,
    LoginUsuarioView,
    LogoutUsuarioView,
    PerfilView,
    ListarUsuariosView,
    DesactivarUsuarioView
)

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),

    # Perfil
    path('perfil/', PerfilView.as_view(), name='perfil'),
    
    # Gestión de usuarios - Admin
    path('', ListarUsuariosView.as_view(), name='listar-usuarios'),
    path('<int:pk>/toggle-estado/', DesactivarUsuarioView.as_view(), name='toggle-estado'),
]