from .models import * 
from rest_framework import serializers

class CategoriasSerializer(serializers.ModelSerializer):
  class Meta:
    model = CategoriasModel
    fields = "__all__"

class ProductosSerializer(serializers.ModelSerializer):

  imagen_url_full = serializers.CharField(source="imagen_url.url", read_only=True)
  
  class Meta:
    model = ProductosModel
    fields = "__all__"
  
class DireccionesSerializer(serializers.ModelSerializer):
  class Meta:
    model = DireccionesModel
    fields = "__all__"