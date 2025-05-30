from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import estudiante
from .forms import estudianteForm
# Create your views here.

def inicio(request):
    return render(request, 'paginas/index.html')

def nosotros(request):
    return render(request, 'paginas/nostros.html')

def servicios(request):
    return render(request, 'paginas/servicios.html')

def ingresar(request):
    return render(request, 'paginas/ingresar.html')

def estudiantes(request):
    estudiantes = estudiante.objects.all()
    return render(request, 'estudiantes/inicio.html', {'estudiantes':estudiantes})

def crear(request):
    formulario = estudianteForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('estudiantes')
    return render(request, 'estudiantes/crear.html', {'formulario':formulario})

def eliminar(request, id):
    estudianteID = estudiante.objects.get(id=id) #la ID es no mas para q sea una variable diferente identificador
    estudianteID.delete()
    return render(request, 'estudiantes/inicio.html', {'estudiantes':estudiantes})

def editar(request, id):
    estudianteE = estudiante.objects.get(id=id) #la E es no mas para q sea una variable diferente editar
    formulario = estudianteForm(request.POST or None, request.FILES or None, instance=estudianteE)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('estudiantes')
    return render(request, 'estudiantes/editar.html', {'formulario':formulario})