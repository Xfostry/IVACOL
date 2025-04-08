from django.shortcuts import render
#agregado
from django.http import HttpResponse

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