from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from django.contrib.auth import authenticate
from  .models import Task
import json

from .forms import create_task_form
# Create your views here.

# from rest_framework.decorators import api_view,APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser


@api_view(http_method_names=["GET","POST"])
@permission_classes([IsAdminUser,IsAuthenticated])
def adduser(request):
    if request.method =="POST":
        data=request.data
        
        serializer=adduserserializer(data=data)
        
        if serializer.is_valid():
            
            serializer.save()
            response={"msg":"user successfully added","data":serializer.data}
            
            return Response(data=response) 
    else:
            
            return Response({"msg":"add details"})    




@api_view(http_method_names=["GET","POST"])
@permission_classes([AllowAny])  # Allow any user to access this endpoint
def login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            print(user)
            try:
                # global token
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                # If token doesn't exist, create a new one
                token = Token.objects.create(user=user)
            request.session["username"]=username
            d=User.objects.get(username=username)    
            data=Task.objects.filter(member=d) 
            print(data)
            
            response = {"msg": "Login successful", "token": token.key,}
            return Response(data=response)
        else:
            return Response({"msg": "Invalid credentials"})
        
    else:
        return JsonResponse({"msg":"try to login first with post request"})
       

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks(request):
    user = request.user
    
    try:
        tasks = Task.objects.filter(member=user)
        serializer = addtaskserializer(tasks, many=True)
        return Response({"msg": "Your tasks", "tasks": serializer.data})
    except Task.DoesNotExist:
        return Response({"msg": "No tasks found for this user"}, status=404)
    except Exception as e:
        return Response({"msg": "An error occurred", "error": str(e)}, status=500)

@permission_classes([IsAuthenticated])   
@api_view(http_method_names=["POST"])       
def reset_password(request):
    username=request.data.get("username")
    password=request.data.get("password")
    print(username)
    try:
        user =User.objects.get(username=username)
    except:
        return Response ({"msg":"user not found"})
    user.set_password(password)
    user.save()
    return Response ({"msg":"password changed successfully"})      
        


 
 
    
@api_view(http_method_names=["GET","POST"])
@permission_classes([IsAdminUser,IsAuthenticated])    
def addtask(request):
    if request.method=="POST":
        data=request.data      
        u=data.get("member")
        t=data.get("task")
        d=data.get("due_date")
        # Check if member username exists
        try:
            user = User.objects.get(username=u)
        except User.DoesNotExist:
            return Response({"error": f"User with username {u} does not exist."}, status=400)
        
        # Create the task
        task = Task.objects.create(task=t, member=user, due_date=d)
        task.save()
        
        
        return Response({"msg":"task successfully added ","name":u})
      
    return Response({"msg":"method not allowed"})
            
        
@api_view(http_method_names=["GET","POST"])
@permission_classes([IsAdminUser,IsAuthenticated])   
def gettask(request,id) :
    if request.method=="GET":
        print(id)
        T=Task.objects.get(id=id)
        print(T.task)
        print("hai")
        
        serializer=addtaskserializer(instance=T)   
        response={"msg":"your tasks","task":serializer.data}
        return Response(data=response)  
    
@permission_classes([IsAdminUser,IsAuthenticated])    
def tasklist(request):
    t=Task.objects.all().values()
    # json_data = json.dumps(list(t))
    return HttpResponse(t)    
    
@permission_classes([IsAdminUser,IsAuthenticated])
def deletetask(request,id):   
    t=Task.objects.get(id=id)
    print(t.member)
    t.delete()
    return JsonResponse({"msg":"deleted successfully"}) 


@permission_classes([IsAdminUser,IsAuthenticated])
def create_task(request):
    if request.method=="POST":
        form=create_task_form(request.POST)
        if form.is_valid():
            task=form.cleaned_data["task"]
            member_id=form.cleaned_data["member_id"]
            due_date=form.cleaned_data["due_date"] 
            print(task)
            print(member_id)
            print(due_date)
            t=Task.objects.create(task=task,member_id=member_id,due_date=due_date)
            t.save()
            return HttpResponse("task added successfully")
               
    form=create_task_form()
    print("hai")
    return render(request,"home.html",{"form":form}) 


@permission_classes([IsAuthenticated])
def logout(request):
    # request.session.flush()
    try:
        del request.session["username"]
        # return Response({"msg":"successfull logged out"})
        return JsonResponse({"msg":"successfull logged out"})
    except:
        return JsonResponse({"msg":"no user is active to logout"})
    
    
    


