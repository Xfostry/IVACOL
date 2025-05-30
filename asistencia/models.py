from django.db import models

# Create your models here.


#toca crear las cosas como en el sql (usuarios, facturas, etc)

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


    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.nodocumento})"

def __str__(self):
        return str(self.id) + " " + self.nombre + " " + self.apellido
    
def delete(self, using = None, keep_parents = False):
    self.foto.storage.delete(self.foto.name)
    super().delete()