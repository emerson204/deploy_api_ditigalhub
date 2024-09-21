from rest_framework import generics , status
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response


class UserRegisterListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Listado de usuarios", 
      "data": response.data 
    })

    
class UserRegisterCreateView(generics.CreateAPIView):
  serializer_class = UserSerializer
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)

    return Response({
      "message": "Registro exitoso",
      "data": response.data
    }, status=status.HTTP_201_CREATED)