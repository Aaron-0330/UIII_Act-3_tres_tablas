# app_uber/urls.py (Archivo nuevo)
from django.urls import path
from . import views

urlpatterns = [
    # 🔹 URL para la función de inicio
    path('', views.inicio_uber, name='inicio_uber'),
    
    # 🔹 URLs para el CRUD de UsuarioPasajero (Punto 24)
    path('usuario_pasajero/agregar/', views.agregar_usuario_pasajero, name='agregar_usuario_pasajero'),
    path('usuario_pasajero/ver/', views.ver_usuario_pasajero, name='ver_usuario_pasajero'),
    path('usuario_pasajero/actualizar/<int:pk>/', views.actualizar_usuario_pasajero, name='actualizar_usuario_pasajero'),
    path('usuario_pasajero/realizar_actualizacion/<int:pk>/', views.realizar_actualizacion_usuario_pasajero, name='realizar_actualizacion_usuario_pasajero'),
    path('usuario_pasajero/borrar/<int:pk>/', views.borrar_usuario_pasajero, name='borrar_usuario_pasajero'),
]