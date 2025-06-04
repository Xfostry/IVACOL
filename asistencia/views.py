from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import usuario, FacturaSubida
from .forms import usuarioForm
from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')  # Cambia 'login' por el nombre de tu url de login si es diferente
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

@login_required
def paginaPrincipal(request):
    return render (request,'paginas/paginaPrincipal.html')

@login_required
def perfil(request):
    from .models import usuario
    try:
        usuario_obj = usuario.objects.get(nodocumento=request.user.username)
    except usuario.DoesNotExist:
        usuario_obj = None
    return render(request, 'paginas/perfil.html', {'usuario': usuario_obj})

@login_required
def graficas(request):
    return render (request,'paginas/graficas.html')

@login_required
def leerFacturas(request):
    return render (request,'paginas/leerFacturas.html')

@login_required
def notificaciones(request):
    return render (request,'paginas/notificaciones.html')

def facturasAdmin(request):
    return render (request,'paginas/facturasAdmin.html')

def UsuariosAdm(request):
    usuarios = usuario.objects.all()
    return render(request, 'ingresos/InicioAdm.html', {'usuarios':usuarios})
def CrudAdm(request):
    Usuario = usuario.objects.get(id=id) #la E es no mas para q sea una variable diferente editar
    formulario = usuarioForm(request.POST or None, request.FILES or None, instance=Usuario)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('CrudAdm')
    return render(request, 'ingresos/crudAdm.html', {'formulario':formulario})

def InicioAdm(request):
    usuarios = usuario.objects.all()
    return render (request,'ingresos/InicioAdm.html', {'usuarios': usuarios})

def editarAdm(request, id):
    UsuarioE = usuario.objects.get(id=id) #la E es no mas para q sea una variable diferente editar
    formulario = usuarioForm(request.POST or None, request.FILES or None, instance=UsuarioE)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('InicioAdm')
    return render(request, 'ingresos/editarAdm.html', {'formulario':formulario})

def eliminarAdm(request, id):
    usuario.objects.get(id=id).delete()
    return redirect('InicioAdm')

def CrearAdm(request):
    formulario = usuarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('InicioAdm')
    return render(request, 'ingresos/crearAdm.html', {'formulario':formulario})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login # Renombrar login para evitar conflicto
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import LoginForm



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('paginaPrincipal') 
                else:
                    messages.error(request, "Usuario inactivo")
            else:
                messages.error(request, "Credenciales inválidas")
        #si falla validación del form o de las credenciales se renderiza de nuevo con errores
    else:
        form = LoginForm()

    return render(request, "paginas/login.html", {"form": form})


def historial_facturas(request):
    """
    Muestra el historial de facturas del usuario logueado, más recientes primero.
    """
    # Filtrar solo las facturas del usuario autenticado
    facturas_usuario = FacturaSubida.objects.filter(usuario=request.user).order_by('-fecha_subida')
    context = {
        'facturas': facturas_usuario,
        'titulo_pagina': 'Historial de Facturas Subidas'
    }
    return render(request, 'paginas/historial_facturas.html', context)



from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def registrarse(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        doc_type = request.POST['doc_type']
        doc_number = request.POST['doc_number']
        gender = request.POST['gender']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']

        # Validaciones básicas (puedes agregar más)
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registrarse')
        if User.objects.filter(username=doc_number).exists():
            messages.error(request, 'Ya existe un usuario con ese número de documento.')
            return redirect('registrarse')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
            return redirect('registrarse')

        user = User.objects.create_user(
            username=doc_number,
            email=email,
            password=password,
            first_name=fullname
        )

        # Crear el usuario en el modelo personalizado
        from .models import usuario
        usuario.objects.create(
            nombres=fullname,
            apellidos="",  # Si tienes un campo para apellidos separado, sepáralo de fullname
            idtipodocumento=1,  # Ajusta según tu lógica de tipos de documento
            nodocumento=doc_number,
            idgenero=1,  # Ajusta según tu lógica de géneros
            idciudad=1,  # Ajusta según tu lógica de ciudades
            numero=phone,
            correo=email,
            contrasena=password,  # Lo ideal es guardar la contraseña encriptada o dejarla vacía aquí
            direccion=address,
            idrol=2,  # Ajusta según tu lógica de roles
            # fechaIngreso se puede dejar en blanco o poner la fecha actual
        )

        messages.success(request, 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'paginas/registrarse.html')























"""def login_view(request):
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
            # Formulario inválido (ej: campos vacíos si no validaste en cliente, u otros errores)
            # Los errores ya están en el objeto 'form'
             messages.error(request, 'Por favor corrige los errores indicados.') # Mensaje genérico opcional
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
    return render(request, 'paginas/historial_facturas.html')"""




