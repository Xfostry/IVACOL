from django.urls import path
from . import views
# Tambien para ver las fotos en el crud
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('estudiantes/', views.estudiantes, name='estudiantes'),
    path('estudiantes/crear', views.crear, name='crear'),
    # path('editar/', views.editar, name='editar'),    CREAMOS OTRO PA VERIFICAR SI SIRVE
    path('editar/<int:id>', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
