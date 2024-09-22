from .models import *
from .serializer import *
from rest_framework import generics , status, serializers
from rest_framework.response import Response
from django.http import Http404

from almacen.serializer import  ProductosSerializer
from almacen.models import ProductosModel
from .serializer import OrderSerializer, OrdenesSerializerResponse, OrdenDetalleSerializerResponse, ProcessPaymentSerializer
from django.db import transaction

import requests

class OrdenesListView(generics.ListAPIView):
  queryset = OrdenesModel.objects.all()
  serializer_class = OrdenesSerializer
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Listado de Ordenes",
      "data": response.data
    },status=status.HTTP_200_OK)
  

class OrdenesCreateView(generics.CreateAPIView):
    serializer_class = OrdenesSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            details = validated_data.get('details', [])

            if not details:
                return Response({
                    "message": "Debe especificar al menos un detalle de la orden",
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validar el precio y restar el stock
            total_price = 0
            error_products = []
            order_details = []
            is_error = False
            
            with transaction.atomic():
              # Crear la orden correctamente con OrdenesModel
              new_order = OrdenesModel.objects.create(
                  usuario=validated_data.get('usuario'),
                  fecha_orden=validated_data.get('fecha_orden'),
                  total=total_price,
              )

              for detail in details:
                  producto = detail.get('producto_id')

                  if producto:
                      # Validar stock y estado del producto
                      if producto.stock < detail.get('cantidad') or producto.estado == False:
                          is_error = True
                          error_products.append(producto)

                      if is_error == False:
                          # Crear detalle de la orden asignando IDs en lugar de objetos
                          new_order_detail = OrdenDetailModel.objects.create(
                              cantidad=int(detail.get('cantidad')),
                              precio=producto.precio,
                              subtotal=producto.precio * int(detail.get('cantidad')),
                              producto_id=producto, 
                              orden_id=new_order,  
                          )
                          order_details.append(new_order_detail)

                          # Actualizar el precio total y ajustar el stock
                          total_price += producto.precio * detail.get('cantidad')
                          producto.stock -= detail.get('cantidad')
                          producto.save()

                          if producto.stock < 0:
                             is_error = True
                             error_products.append(producto)
                     
              # Verificar si hubo errores en productos
              else:
                  new_order.total = total_price
                  new_order.save() 

                  if is_error == True:
                    product_serializes = ProductosSerializer(error_products, many=True).data
                    return Response({
                        'message': 'No es posible continuar con el pago, algunos productos presentan inconsistencias',
                        'data': {
                            'error': product_serializes
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Serializar la orden y los detalles de la orden
          
      
            order_details_serializado = OrdenDetalleSerializerResponse(order_details, many=True).data
            order_serilizado = OrderSerializer(new_order).data

            return Response({
                "message": "Orden Creada Correctamente",
                'total_price': total_price,
                'order': order_serilizado,
                'order_details': order_details_serializado,
            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
         return Response({
            "message": "Datos inválidos",
            "error": e.detail  
         },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": "Ocurrió un error inesperado",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProcessPayment(generics.CreateAPIView):
  serializer_class = ProcessPaymentSerializer

  def create(self, request, *args, **kwargs):
    try:
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({
                "message": "Datos inválidos",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        order_id = validated_data.get('order_id',None)
        token_id = validated_data.get('token_id',None)

        order = OrdenesModel.objects.filter(id=order_id).first()
        
        if not order:
            return Response({
              "message": "Orden no encontrada"
            },status=status.HTTP_404_NOT_FOUND)

        
        amount = int(order.total * 100)  # Convertir a céntimos, por ejemplo, 100.00 soles -> 10000 céntim
        
        # Crear el payload para la solicitud a Culqi
        data = {
          "amount": amount,  # El monto en céntimos 
          "currency_code": "PEN",  # Moneda (PEN o USD)
           "email": "skinnydelocos@gmail.com", # Email del cliente
          "source_id": token_id,  # El token que se generó en el frontend
          "description": "Pago por producto",  # Descripción del cargo
          "capture": True, # Indica que la captura sea automatico, (12.00 am) procesa culqi
        }
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer sk_test_741afc9912d8355f"
        }
    
        response = requests.post(
          'https://api.culqi.com/v2/charges',  # Api
          json=data,
          headers=headers
        )
        
        response_data = response.json()
        
        if response.status_code == 201:
          return Response({
            "message": "Pago realizado con éxito",
            "data": response_data
          })

        return Response({
            "message": "Hubo un problema al realizar el pago",
            "error": response_data
        })
    except Exception as e:
        return Response({
            "message": "Ocurrió un error inesperado",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrdenesUpdateView(generics.UpdateAPIView):
  queryset = OrdenesModel.objects.all()
  serializer_class = OrdenesSerializer
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Orden Actualizada Correctamente",
        "data": response.data
      },status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Orden no encontrada"
      },status=status.HTTP_404_NOT_FOUND)
    
class OrdenesDeleteView(generics.DestroyAPIView):
  queryset = OrdenesModel.objects.all()
  
  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.estado = False
      instance.save()
      
      serializer = self.get_serializer()
      
      return Response({
        "message": "Orden Eliminada Correctamente",
        "data": serializer.data
      },status=status.HTTP_200_OK)
    
    except Http404:
      return Response({
        "message": "Orden no encontrada"
      },status=status.HTTP_404_NOT_FOUND)
    
# VISTAS PARA TRANSACCIONES DE PAGOS

class PagosListView(generics.ListAPIView):
  queryset = PagosModel.objects.all()
  serializer_class = PagosSerializer
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Listado de Pagos",
      "data": response.data
    },status=status.HTTP_200_OK)
    

  
class PagosUpdateView(generics.UpdateAPIView):
  queryset = PagosModel.objects.all()
  serializer_class = PagosSerializer
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)

      return Response({
        "message" : "Orden Actualizada Correctamente",
        "data": response.data
      },status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Orden no encontrada"
      },status=status.HTTP_404_NOT_FOUND)
      
class PagosDeleteView(generics.DestroyAPIView):
  queryset = PagosModel.objects.all()
  
  def destroy(self, request, *args, **kwargs):
    try:
      super().destroy(request, *args, **kwargs)
      
      return Response({
        "message": "Orden Eliminada Correctamente"
      }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        "message": "Orden no encontrada"
      },status=status.HTTP_404_NOT_FOUND)