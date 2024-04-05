from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import ChatMessageSerializer
from.models import ChatMessage
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from django.contrib.auth import authenticate
# from  .models import Task
import json

# from .forms import create_task_form
# Create your views here.

# from rest_framework.decorators import api_view,APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

@permission_classes([IsAuthenticated])
class ChatroomView(APIView):
    def get(self, request):
        messages = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        data=request.data
        u=data.get("user")
        m=data.get("message")
        user=User.objects.get(username=u)
        print(user.id)
        user_id=user.id
        message=ChatMessage.objects.create(user=user,message=m)
        message.save()
        response={"msg":"created"}
        return Response(data=response)