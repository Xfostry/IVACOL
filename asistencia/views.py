from django.shortcuts import render
#agregado
from django.http import HttpResponse
from django.contrib.auth.models import User

def inicio(request):
    return render(request, 'paginas/index.html')

def alinicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render (request,'paginas/nosotros.html')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def presentacion(request):
    return render (request,'paginas/presentacion.html')

def login(request):
    return render (request,'paginas/login.html')

def registrarse(request):
    return render (request,'paginas/registrarse.html')

def crud(request):
    return render (request,'paginas/crud.html')

def contactenos(request):
    return render (request,'paginas/contactenos.html')

def diccionario(request):
    return render (request,'paginas/diccionario.html')

def dml(request):
    return render (request,'paginas/dml.html')

def solicitarContra(request):
    return render (request,'paginas/solicitarContraseña.html')

def cambiarContra(request):
    return render (request,'paginas/cambiarContraseña.html')

def confirmarContra(request):
    return render (request,'paginas/confirmarContraseña.html')

def paginaPrincipal(request):
    return render (request,'paginas/paginaPrincipal.html')

def perfil(request):
    return render (request,'paginas/perfil.html')

def graficas(request):
    return render (request,'paginas/graficas.html')

def leerFacturas(request):
    return render (request,'paginas/leerFacturas.html')

def notificaciones(request):
    return render (request,'paginas/notificaciones.html')

def facturasAdmin(request):
    return render (request,'paginas/facturasAdmin.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login # Renombrar login para evitar conflicto
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirigir a la página principal después del login exitoso
                # Cambia 'nombre_url_dashboard' por el name de tu URL principal
                return redirect('nombre_url_dashboard')
            else:
                # Usuario inválido (aunque is_valid pasó, authenticate falló)
                 # AuthenticationForm maneja este error internamente, no se necesita mensaje extra usualmente.
                 # Si usas un form personalizado, aquí pondrías:
                 # messages.error(request, 'Usuario o contraseña incorrectos.')
                 pass # Dejar que el re-renderizado muestre el error del form
        else:
            # Formulario inválido (ej: campos vacíos si no validaste en cliente, u otros errore            # Los errores ya están en el objeto 'form'
             messages.error(request, 'Por favor corrige los errores indicados.') 
    else:
        form = AuthenticationForm() # Formulario vacío para GET

    # Re-renderizar la misma plantilla con el formulario (que puede tener errores)
    return render(request, 'IVACO/asistencia/templates/paginas/login.html', {'form': form})

# Asegúrate de tener una URL mapeada a esta vista en urls.py
# path('login/', views.login_view, name='login'),
# Y una URL para el dashboard
# path('dashboard/', views.dashboard_view, name='nombre_url_dashboard'),


 # Importa tu modelo

# ¡Muy importante para la seguridad!
def historial_facturas(request):
    # Filtra las facturas para obtener solo las del usuario que ha iniciado sesión
    # facturas_usuario = FacturaSubida.objects.filter(usuario=request.user).order_by('-fecha_subida') # Más recientes primero

    # context = {
      #  'facturas': facturas_usuario,
       # 'titulo_pagina': 'Historial de Facturas Subidas'
    # }
    return render(request, 'paginas/historial_facturas.html')




