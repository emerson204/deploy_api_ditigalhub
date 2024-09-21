from django.db import models
from django.contrib.auth.models import User
from almacen.models import ProductosModel

class OrdenesModel(models.Model): 
  id = models.AutoField(primary_key=True)
  usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordenes")
  fecha_orden = models.DateTimeField(auto_now_add=True) # Que fecha que dia que mes , etc , q se ah echo la opreracion
  total = models.FloatField()
  estado = models.BooleanField(default=True) # True o False mas na
  
  class Meta:
    db_table = "ordenes"
    
# Crear detalle de la orden
class OrdenDetailModel(models.Model):
  id = models.AutoField(primary_key=True)
  cantidad = models.IntegerField()
  precio = models.FloatField()
  subtotal = models.FloatField()
  producto_id = models.ForeignKey(ProductosModel, on_delete=models.CASCADE, related_name="orden_detail")
  orden_id = models.ForeignKey(OrdenesModel, on_delete=models.CASCADE, related_name="orden_detail")
  
  class Meta:
    db_table = "orden_detail"

class PagosModel(models.Model):
  id = models.AutoField(primary_key=True)
  orden_id = models.ForeignKey(OrdenesModel, on_delete=models.CASCADE, related_name="pagos")
  fecha_pago = models.DateTimeField(auto_now_add=True)
  cantidad = models.FloatField()
  
  PAYMENT_METHOD_CHOICE = [
    ("CASH", "Efectivo"),
    ("CARD", "Tarjeta")
  ]
  metodo_pago = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICE)
  estado = models.BooleanField(default=True) # True o False
  
  
  class Meta:
    db_table = "pagos"