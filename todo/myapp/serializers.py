from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from rest_framework.authtoken.models import Token



class adduserserializer(serializers.ModelSerializer):
     
    class Meta:
         
         model=User
         fields=["username","password"]
         
         
    def create(self, validated_data):
        print(validated_data)
        # password=validated_data.pop("password")
        password=validated_data["password"]
        print(password)
        user=super().create(validated_data)
        
        user.set_password(password)  # this is used to make hash password
        user.save() 
        print(user)
        token = Token.objects.create(user=user)
        print(token.key)    
        return user
         
         

class addtaskserializer(serializers.ModelSerializer):
     
     class Meta:
        
         
        model=Task
        fields=["member","task","due_date"]     
         
         
             