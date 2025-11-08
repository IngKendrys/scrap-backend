from django.urls import path
from .views import (
    RegistroUsuarioView,
    LoginUsuarioView,
    LogoutUsuarioView,
    ListarUsuariosView,
    DesactivarUsuarioView,
    ActualizarUsuarioView
)

app_name = 'usuarios'

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('actualizar/<int:pk>/', ActualizarUsuarioView.as_view(), name='actualizar-usuario'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),

    path('', ListarUsuariosView.as_view(), name='listar-usuarios'),
    path('estado/<int:pk>/', DesactivarUsuarioView.as_view(), name='toggle-estado'),
]