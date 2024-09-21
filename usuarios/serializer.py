from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): 
  
  password = serializers.CharField(write_only=True)
  
  class Meta : 
    model = User
    fields = ["username","password","email","first_name","last_name"]
    
    extra_kwargs = {
      "username": {"required": True},
      "password": {"required": True},
      "email": {"required": True},
      "first_name": {"required": True},
      "last_name": {"required": True}
    }
    
  def create(self, validated_data):
    user = User.objects.create_user(
      username = validated_data["username"],
      password = validated_data["password"],
      email = validated_data["email"],
      first_name = validated_data["first_name"],
      last_name = validated_data["last_name"]
    )
    return user