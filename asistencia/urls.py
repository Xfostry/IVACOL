from django.urls import path
from . import views

urlpatterns = [
    path('subir_factura/', views.subir_factura, name='subir_factura'),
    path('borrar_factura/<int:id>/', views.borrar_factura, name='borrar_factura'),
    path('editar_factura/<int:id>/', views.editar_factura, name='editar_factura'),
    path('descargar_facturas_pdf/', views.descargar_facturas_pdf, name='descargar_facturas_pdf'),
    path('get_facturas_usuario/', views.get_facturas_usuario, name='get_facturas_usuario'),
]
