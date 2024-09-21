from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class CategoriasModel(models.Model):
  id = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=200)
  descripcion = models.TextField()
  slug = models.CharField(max_length=50)
  estado = models.BooleanField(default=True)
  
  class Meta:
    db_table = "categorias"
  
class ProductosModel(models.Model):
  id = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=200)
  descripcion = models.TextField()
  precio = models.FloatField()
  stock = models.IntegerField()
  categoria_id = models.ForeignKey(CategoriasModel, on_delete=models.CASCADE, related_name="productos")
  imagen_url = CloudinaryField('image', blank=True, null=True) # Aca se guardara la imagen , ejm (imagen.png)
  imagen_url_full = models.URLField(blank=True , null=True) # Aca se guardara la url ejm (www.cloudinary/nube/carpeta/imagen.png)
  slug = models.CharField(max_length=50)
  destacado = models.BooleanField(default=True)
  populares = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True) 
  updated_at = models.DateTimeField(auto_now=True)
  estado = models.BooleanField(default=True)

  class Meta: 
    db_table = "productos"

  
class DireccionesModel(models.Model):
  id = models.AutoField(primary_key=True)
  usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="direcciones")
  direccion = models.TextField()
  ciudad = models.CharField(max_length=100)
  estado = models.BooleanField(default=True)
  
  class Meta: 
    db_table = "direcciones"