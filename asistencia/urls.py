from django.urls import path
from . import views

urlpatterns = [
    path('subir_factura/', views.subir_factura, name='subir_factura'),
    path('borrar_factura/<int:id>/', views.borrar_factura, name='borrar_factura'),
]
