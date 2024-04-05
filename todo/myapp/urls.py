from django.contrib import admin
from django.urls import path,include
from myapp import views
# from chatroom import views

urlpatterns = [
    
    
    

    path("adduser/",views.adduser,name="adduser"),
    path("addtask/",views.addtask,name="addtask"),
    path("<int:id>/",views.gettask,name="gettask"),
    path("tasklist/",views.tasklist,name="tasklist"),
    path("deletetask/<int:id>/",views.deletetask,name="deletetask"),
    
    
    
]