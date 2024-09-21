from .models import *
from .serializer import *
from rest_framework import generics , status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

# VISTA DE CATEGORIAS 
class CategoriasListView(generics.ListAPIView):
  queryset = CategoriasModel.objects.all()
  serializer_class = CategoriasSerializer
  permission_classes = [IsAuthenticated]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)  

    return Response({
      "message": "Listado de Categorias",
      "data": response.data
    }, status=status.HTTP_200_OK)
  
class CategoriasCreateView(generics.CreateAPIView):
  serializer_class = CategoriasSerializer
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Creado Correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
    
class CategoriasUpdateView(generics.UpdateAPIView):
  queryset = CategoriasModel.objects.all()
  serializer_class = CategoriasSerializer
  
  def update(self, request, *args, **kwargs):
    try:       
      response = super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Actualizado Correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Categoria no encontrada"
      }, status=status.HTTP_404_NOT_FOUND)

class CategoriasDeleteView(generics.DestroyAPIView):
  queryset = CategoriasModel.objects.all()
  serializer_class =  CategoriasSerializer
  
  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.estado = False
      instance.save()
      
      serializer = self.get_serializer()
      
      return Response({
        "message": "Categoria Eliminada Correctamente",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Categoria no encontrada"
      }, status=status.HTTP_404_NOT_FOUND)
      
    
# VISTA DE PRODUCTOS

class ProductosListView(generics.ListAPIView):
  queryset = ProductosModel.objects.all()
  serializer_class = ProductosSerializer
  permission_classes = [IsAuthenticated]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
      
    return Response({
      "message": "Listado de Productos",
      "data": response.data
    },status=status.HTTP_200_OK)
    
class ProductosCreateView(generics.CreateAPIView):
    serializer_class = ProductosSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Guardar el producto sin la URL completa aún
            producto = serializer.save()
            
            # Obtener la URL completa de Cloudinary
            img_url_full = producto.imagen_url.url  # Suponiendo que img_url es el campo en tu modelo
            
            # Actualizar el campo img_url_full en el producto
            producto.imagen_url_full = img_url_full
            producto.save()
            
            # Serializar el producto actualizado
            response_serializer = ProductosSerializer(producto)
            
            return Response({
                "message": "Producto creado correctamente",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductosUpdateView(generics.UpdateAPIView):
  queryset = ProductosModel.objects.all()
  serializer_class = ProductosSerializer
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)

      return Response({
        "message": "Producto Actualizado Correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)

    except Http404:
      return Response({
        "message": "Producto no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
      
class ProductosDeleteView(generics.DestroyAPIView):
  queryset = ProductosModel.objects.all()
  serializer_class =  ProductosSerializer
  
  def destroy(self, request, *args, **kwargs):
    try:
      print(kwargs.get("pk"))
      instance = self.get_object()
      instance.estado = False
      instance.save()
      
      
      serializer = self.get_serializer(instance)

      return Response({
        "message": "Producto Eliminado Correctamente",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Http404:
      return Response({
        "message" : "Producto no encontrado"
      },status=status.HTTP_404_NOT_FOUND)
    
# Vista de direcciones 

class DireccionesListView(generics.ListAPIView):
  queryset = DireccionesModel.objects.all()
  serializer_class = DireccionesSerializer
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Listado de Direcciones",
      "data": response.data
    },status=status.HTTP_200_OK)
  
class DireccionesCreateView(generics.CreateAPIView):
  serializer_class = DireccionesSerializer
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Dirección Creada Correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
  
class DireccionesUpdateView(generics.UpdateAPIView):
  queryset = DireccionesModel.objects.all()
  serializer_class = DireccionesSerializer
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Dirección Actualizada Correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
    
    except Http404:
      return Response({
        "message": "Dirección no encontrada"
      }, status=status.HTTP_404_NOT_FOUND)
  
class DireccionesDeleteView(generics.DestroyAPIView):
  queryset = DireccionesModel.objects.all()
  serializer_class = DireccionesSerializer
  
  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.estado = False
      instance.save()
      
      serializer = self.get_serializer()
      
      return Response({
        "message": "Dirección Eliminada Correctamente",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Http404:
      return Response({
        "message" : "Dirección no encontrada"
      },status=status.HTTP_404_NOT_FOUND)
  
