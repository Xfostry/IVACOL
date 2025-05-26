from django.db import models

# Create your models here.


#toca crear las cosas como en el sql (usuarios, facturas, etc)

#class estudiante(models.Model):
 #   id = models.AutoField(primary_key=True)
  #  nombre = models.CharField(max_length=50, verbose_name="Nombre")
   # apellido = models.CharField(max_length=50, verbose_name="Apellido")
    #foto = models.ImageField(upload_to='fotos/', verbose_name="Foto", null=True)
    #clase=models.TextField(verbose_name="Clase", null=True)
    #direccion = models.CharField(max_length=50, verbose_name="Dirección", blank=True, null=True)
    #fechaIngreso = models.DateField(verbose_name="Fecha Ingreso", blank=True, null=True)

def __str__(self):
        return str(self.id) + " " + self.nombre + " " + self.apellido
    
def delete(self, using = None, keep_parents = False):
    self.foto.storage.delete(self.foto.name)
    super().delete()