from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=30, unique=True)
    genero = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    rol = models.CharField(max_length=20)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} ({self.numero_documento})'

class FacturaSubida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    numero = models.CharField(max_length=50)
    nit = models.CharField(max_length=50)
    fecha = models.DateField(null=True, blank=True)
    categoria = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=30, decimal_places=15)
    tipo_monto = models.CharField(max_length=20, default='neto')
    archivo = models.FileField(upload_to='facturas/', null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Factura {self.numero} de {self.usuario}'