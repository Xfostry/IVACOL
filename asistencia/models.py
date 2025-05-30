from django.db import models

# Modelos para el sistema IVACOL

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

def __str__(self):
        return str(self.id) + " " + self.nombre + " " + self.apellido
    
def delete(self, using = None, keep_parents = False):
    self.foto.storage.delete(self.foto.name)
    super().delete()
