# app_uber/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import UsuarioPasajero
from datetime import date # Necesario para la fecha de registro
import re # Módulo para validación básica de email/teléfono si fuera necesario, aunque no se pide validación estricta (Punto 28)
# app_uber/views.py

# 🔹 Vista de Inicio (Punto 14)
def inicio_uber(request):
    # Por ahora solo carga el template inicio.html
    return render(request, 'inicio.html')

# 🔹 Vistas del CRUD de UsuarioPasajero (Punto 14)
def agregar_usuario_pasajero(request):
    # Lógica para agregar
    return render(request, 'usuario_pasajero/agregar_usuario_pasajero.html')

def ver_usuario_pasajero(request):
    # Lógica para mostrar todos
    pasajeros = UsuarioPasajero.objects.all()
    return render(request, 'usuario_pasajero/ver_usuario_pasajero.html', {'pasajeros': pasajeros})

def actualizar_usuario_pasajero(request, pk):
    # Lógica para obtener datos antes de la actualización
    return render(request, 'usuario_pasajero/actualizar_usuario_pasajero.html')

def realizar_actualizacion_usuario_pasajero(request, pk):
    # Lógica para procesar la actualización
    # Esto debería redirigir a alguna página después de la actualización
    return redirect('ver_usuario_pasajero') 

def borrar_usuario_pasajero(request, pk):
    # Lógica para borrar
    return render(request, 'usuario_pasajero/borrar_usuario_pasajero.html')
# =========================================================
# VISTAS DE NAVEGACIÓN
# =========================================================
# (Punto 14)
def inicio_uber(request):
    """Muestra la página de inicio."""
    return render(request, 'inicio.html')


# =========================================================
# VISTAS CRUD - USUARIO PASAJERO (Punto 14)
# =========================================================

# 1. Agregar Usuario Pasajero
def agregar_usuario_pasajero(request):
    """Permite registrar un nuevo Usuario Pasajero."""
    if request.method == 'POST':
        # 🔹 No se usa forms.py (Punto 23), se recupera directamente del POST
        try:
            # Crea y guarda la instancia del modelo con los datos del formulario
            UsuarioPasajero.objects.create(
                nombre=request.POST['nombre'],
                email=request.POST['email'],
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion'],
                # 🔹 Se asume que la fecha de registro es la fecha actual
                fecha_registro=date.today(), 
                genero=request.POST['genero'],
                ciudad=request.POST['ciudad'],
            )
            # Redirige a la lista después de guardar
            return redirect('ver_usuario_pasajero')
        except IntegrityError:
            # Manejo básico de error de duplicado (ej. email)
            context = {
                'error': 'Error: El email o algún otro campo único ya existe.',
                'nombre': request.POST.get('nombre', ''),
                'email': request.POST.get('email', ''),
                'telefono': request.POST.get('telefono', ''),
                'direccion': request.POST.get('direccion', ''),
                'genero': request.POST.get('genero', ''),
                'ciudad': request.POST.get('ciudad', ''),
            }
            return render(request, 'usuario_pasajero/agregar_usuario_pasajero.html', context)
        except Exception as e:
             # Manejo de otros errores
            context = {
                'error': f'Error al guardar: {e}',
                'nombre': request.POST.get('nombre', ''),
                'email': request.POST.get('email', ''),
                'telefono': request.POST.get('telefono', ''),
                'direccion': request.POST.get('direccion', ''),
                'genero': request.POST.get('genero', ''),
                'ciudad': request.POST.get('ciudad', ''),
            }
            return render(request, 'usuario_pasajero/agregar_usuario_pasajero.html', context)

    # Si es GET, simplemente muestra el formulario vacío
    return render(request, 'usuario_pasajero/agregar_usuario_pasajero.html')

# 2. Ver Usuario Pasajero (Listar)
def ver_usuario_pasajero(request):
    """Muestra la lista de todos los Usuarios Pasajeros."""
    # Obtiene todos los objetos del modelo
    pasajeros = UsuarioPasajero.objects.all().order_by('nombre')
    context = {'pasajeros': pasajeros}
    return render(request, 'usuario_pasajero/ver_usuario_pasajero.html', context)

# 3. Vista de Formulario de Actualización
def actualizar_usuario_pasajero(request, pk):
    """Muestra el formulario con los datos del Usuario Pasajero a editar."""
    # Obtiene el objeto, o devuelve 404 si no existe
    pasajero = get_object_or_404(UsuarioPasajero, pk=pk)
    context = {'pasajero': pasajero}
    return render(request, 'usuario_pasajero/actualizar_usuario_pasajero.html', context)

# 4. Procesar la Actualización (realizar_actualizacion_usuario_pasajero)
def realizar_actualizacion_usuario_pasajero(request, pk):
    """Procesa los datos del formulario de actualización y guarda los cambios."""
    if request.method == 'POST':
        # Obtiene el objeto, o devuelve 404 si no existe
        pasajero = get_object_or_404(UsuarioPasajero, pk=pk)
        
        try:
            # 🔹 Actualiza los campos directamente
            pasajero.nombre = request.POST['nombre']
            # Validación simple de unicidad antes de actualizar
            if UsuarioPasajero.objects.filter(email=request.POST['email']).exclude(pk=pk).exists():
                 raise IntegrityError("El email proporcionado ya está en uso por otro usuario.")
                 
            pasajero.email = request.POST['email']
            pasajero.telefono = request.POST['telefono']
            pasajero.direccion = request.POST['direccion']
            pasajero.genero = request.POST['genero']
            pasajero.ciudad = request.POST['ciudad']
            
            pasajero.save() # Guarda los cambios
            
            # Redirige a la vista de la lista o detalle después de la actualización
            return redirect('ver_usuario_pasajero')
        
        except IntegrityError as e:
            # Manejo de error de duplicado (ej. email)
            context = {'pasajero': pasajero, 'error': f'Error al actualizar: {e.args[0]}'}
            return render(request, 'usuario_pasajero/actualizar_usuario_pasajero.html', context)
        except Exception as e:
            # Manejo de otros errores
            context = {'pasajero': pasajero, 'error': f'Error inesperado: {e}'}
            return render(request, 'usuario_pasajero/actualizar_usuario_pasajero.html', context)
            
    # Si no es POST, redirige al formulario de edición (debería ser GET)
    return redirect('actualizar_usuario_pasajero', pk=pk)


# 5. Borrar Usuario Pasajero
def borrar_usuario_pasajero(request, pk):
    """Muestra la página de confirmación para borrar un Usuario Pasajero."""
    pasajero = get_object_or_404(UsuarioPasajero, pk=pk)
    
    if request.method == 'POST':
        # Si se confirma la eliminación
        pasajero.delete()
        # Redirige a la lista después de borrar
        return redirect('ver_usuario_pasajero')
        
    # Si es GET, muestra la página de confirmación
    context = {'pasajero': pasajero}
    return render(request, 'usuario_pasajero/borrar_usuario_pasajero.html', context)

# Vistas de Chofer y Viajes (Pendientes por el punto 27)
# ...