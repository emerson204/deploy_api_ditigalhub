from django.contrib import admin
from .models import *

class CategoriasModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'nombre', 'descripcion' , 'slug')

admin.site.register(CategoriasModel)
admin.site.register(ProductosModel)
admin.site.register(DireccionesModel)