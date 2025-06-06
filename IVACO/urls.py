"""
URL configuration for IVACO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from asistencia import views
from asistencia.views import user_login

# Tambien para ver las fotos en el crud
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'asistencia.views.error_404_view'  # Se debe referenciar como string

#esto se ve en views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.alinicio, name= 'inicio'),
    path('index/', views.inicio, name='index'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('presentacion/', views.presentacion, name='presentacion'), 
    #path('login/', views.login, name='login'), Es
    path('registrarse/', views.registrarse, name='registrarse'),
    path('crud/', views.crud, name='crud'),
    path('contactenos/', views.contactenos, name='contactenos'),
    path('diccionario/', views.diccionario, name='diccionario'),
    path('dml/', views.dml, name='dml'),
    path('solicitarContraseña/', views.solicitarContra, name='solicitarContra'),
    path('cambiarContraseña/', views.cambiarContra, name='cambiarContra'),  
    path('confirmarContraseña/', views.confirmarContra, name='confirmarContra'),
    path('paginaPrincipal/', views.paginaPrincipal, name='paginaPrincipal'),
    path('historial_facturas/', views.historial_facturas, name='historial_facturas'),
    path('perfil/', views.perfil, name='perfil'),
    path('graficas/', views.graficas, name='graficas'),
    path('leerFacturas/', views.leerFacturas, name='leerFacturas'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('facturasAdmin/', views.facturasAdmin, name='facturasAdmin'),
    path('CrudAdm/', views.CrudAdm, name='CrudAdm'),
    path('UsuariosAdm/', views.UsuariosAdm, name='UsuariosAdm'),
    path('InicioAdm/', views.InicioAdm, name='InicioAdm'),
    path('CrearAdm/', views.CrearAdm, name='CrearAdm'),
    path('editarAdm/<int:id>', views.editarAdm, name='editarAdm'),
    path('eliminarAdm/<int:id>', views.eliminarAdm, name='eliminarAdm'),
    path('login/', user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('asistencia/', include('asistencia.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)