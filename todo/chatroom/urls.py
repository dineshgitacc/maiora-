from django.urls import path
from. import views

urlpatterns = [
    path('', views.ChatroomView.as_view(), name='chatroom-api'),
]