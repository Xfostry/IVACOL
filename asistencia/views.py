from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import usuario, FacturaSubida
from .forms import usuarioForm
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import get_object_or_404

@csrf_exempt
@login_required
def subir_factura(request):
    if request.method == 'POST':
        try:
            usuario_obj = usuario.objects.get(nodocumento=request.user.username)
        except usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=400)

        descripcion = request.POST.get('invoice-description', '')
        numero = request.POST.get('invoice-number', '')
        nit = request.POST.get('invoice-nit', '')
        fecha = request.POST.get('invoice-date', '')
        categoria = request.POST.get('invoice-category', '')
        monto = request.POST.get('invoice-amount', '')
        tipo_monto = request.POST.get('amount-type', 'neto')
        archivo = request.FILES.get('invoice-file', None)

        try:
            monto_decimal = float(monto)
        except Exception:
            monto_decimal = 0

        factura = FacturaSubida(
            usuario=usuario_obj,
            descripcion=descripcion,
            numero=numero,
            nit=nit,
            fecha=fecha if fecha else None,
            categoria=categoria,
            monto=monto_decimal,
            tipo_monto=tipo_monto,
        )
        if archivo:
            factura.archivo = archivo
        factura.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

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


@login_required
def historial_facturas(request):
    from .models import usuario, FacturaSubida
    try:
        usuario_obj = usuario.objects.get(nodocumento=request.user.username)
    except usuario.DoesNotExist:
        usuario_obj = None

    facturas_usuario = FacturaSubida.objects.filter(usuario=usuario_obj).order_by('-fecha_subida') if usuario_obj else []
    facturas_context = []
    for f in facturas_usuario:
        iva = float(f.monto) * 0.19
        total = float(f.monto) + iva
        facturas_context.append({
            'id': f.id,
            'fecha': f.fecha,
            'numero': f.numero,
            'descripcion': f.descripcion,
            'nit': f.nit,
            'categoria': f.categoria,
            'monto': f.monto,
            'iva': iva,
            'total': total,
        })
    context = {
        'facturas': facturas_context,
        'titulo_pagina': 'Historial de Facturas Subidas'
    }
    return render(request, 'paginas/historial_facturas.html', context)

@login_required
def borrar_factura(request, id):
    from .models import usuario, FacturaSubida
    try:
        usuario_obj = usuario.objects.get(nodocumento=request.user.username)
    except usuario.DoesNotExist:
        return redirect('historial_facturas')
    factura = get_object_or_404(FacturaSubida, usuario=usuario_obj, id=id)
    if request.method == 'POST':
        factura.delete()
        return redirect('historial_facturas')
    return redirect('historial_facturas')



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





















