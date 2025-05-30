from django.db import models

# Modelos para el sistema IVACOL
class usuario(models.Model):
    id = models.AutoField(primary_key=True, help_text='identificador del usuario')
    nombres = models.CharField(max_length=100, help_text='nombre del usuario')
    apellidos = models.CharField(max_length=100, help_text='apellido del usuario')
    idtipodocumento = models.IntegerField(help_text='identificador del tipo de documento')
    nodocumento = models.CharField(max_length=20, unique=True, help_text='numero de documento')
    idgenero = models.IntegerField(help_text='identificador de genero')
    idciudad = models.IntegerField(help_text='identificador de la ciudad')
    numero = models.CharField(max_length=20, help_text='numero de contacto')
    correo = models.EmailField(max_length=100, unique=True, help_text='correo del usuario')
    contrasena = models.CharField(max_length=255, help_text='contrasena encriptada')
    direccion = models.CharField(max_length=100, help_text='direccion del usuario')
    idrol = models.IntegerField(help_text='identificador del rol')
    fechaIngreso = models.DateField(verbose_name="Fecha Ingreso", blank=True, null=True)

class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    tipo_documento = models.CharField(max_length=20, verbose_name="Tipo de Documento")
    no_documento = models.CharField(max_length=20, unique=True, verbose_name="Número de Documento")
    genero = models.CharField(max_length=20, verbose_name="Género")
    ciudad = models.CharField(max_length=50, verbose_name="Ciudad")
    numero = models.CharField(max_length=20, verbose_name="Número de Contacto")
    correo = models.EmailField(max_length=100, unique=True, verbose_name="Correo")
    direccion = models.CharField(max_length=100, verbose_name="Dirección")

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.no_documento})"

class Administrador(models.Model):
    id = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="administrador")
    usuario = models.CharField(max_length=50, unique=True, verbose_name="Usuario")
    contrasena = models.CharField(max_length=255, verbose_name="Contraseña")

    def __str__(self):
        return self.nombre

class FacturaSubida(models.Model):
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE, related_name='facturas_subidas')
    archivo = models.FileField(upload_to='facturas/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Factura de {self.usuario.nombres} subida el {self.fecha_subida}"
