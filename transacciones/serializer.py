from .models import *
from rest_framework import serializers

class OrdenDetalleSerializer(serializers.ModelSerializer):
  orden_id = serializers.IntegerField(read_only=True)
  class Meta:
    model = OrdenDetailModel
    fields = "__all__"

class OrdenesSerializer(serializers.ModelSerializer):
  
  details = OrdenDetalleSerializer(many=True)
  
  class Meta:
    model = OrdenesModel
    fields = "__all__"  

class OrdenesSerializerResponse(serializers.ModelSerializer):
  class Meta:
    model = OrdenesModel
    fields = "__all__"  

class OrdenDetalleSerializerResponse(serializers.ModelSerializer):
  class Meta:
    model = OrdenDetailModel
    fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):  
  class Meta:
    model = OrdenesModel
    fields = "__all__"  

class PagosSerializer(serializers.ModelSerializer):
  class Meta:
    model = PagosModel
    fields = "__all__"

class ProcessPaymentSerializer(serializers.Serializer):
  order_id = serializers.CharField()
  token_id = serializers.CharField()