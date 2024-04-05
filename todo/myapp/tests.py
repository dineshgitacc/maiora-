from django.test import TestCase,SimpleTestCase,Client
from django.urls import resolve,reverse
from myapp.views import addtask,adduser,login,gettask
from unittest.mock import patch
from .models import Task
from django.contrib.auth.models import User
import json

# to use fake values for the model use this by installing mixer
from mixer.backend.django import mixer

# for fake browser like client use this Client()

# Create your tests here.

# urls testing

# class testproject(SimpleTestCase):
    
    
#     def test_resolve(self):
#         url=reverse("gettask",args=[2])
#         print(resolve(url))
#         self.assertEquals(resolve(url).func,gettask)
        
#     def test_resolve1(self):
#         url=reverse("addtask")
#         print(resolve(url))
#         self.assertEquals(resolve(url).func,addtask)    
        
        # if we are using class based view we should mention like this
        # self.assertEquals(resolve(url).func.view_class,addtask)   here assume addtask is classbased view
        
        
# view testing        

class Testviews(TestCase):
    
    def test_task_list(self):
        client=Client()
        
        u=User.objects.create(username="rajshes",password="password")
        t=Task.objects.create(task="devops",member_id=u.id,due_date="2024-03-18")
        
        response=client.get(reverse("gettask",args=[1]))
        # response=client.get(reverse("login"))
        print(response)
        self.assertAlmostEqual(response.status_code,200)
        
# class Testviews(TestCase):
    
#     @patch('myapp.views.Task.objects.get')
#     def test_task_list(self, mock_get_task):
#         mock_task = Task(id=2)  # Create a mock Task object
#         mock_get_task.return_value = mock_task  # Mock the get method to return the mock Task object
        
#         client = Client()
#         response = client.get(reverse("gettask", args=[2]))
        
#         self.assertEqual(response.status_code, 200)   
        

class Testviews1(TestCase):
    
    def setUp(self):
        
        self.client=Client()
        self.tasklist_url=reverse("tasklist")
        
    def test_task_list(self):
         
        response=self.client.get(self.tasklist_url)
        # response=client.get(reverse("login"))
        print(response)
        a=10
        b=10
        c=a+b
        # instead of using assertalmost or many asserts commands in normal unit test use only assert after installing pytest
        assert c==20
        
        
        self.assertAlmostEqual(response.status_code,200) 
        
        assert response.status_code==200
        
    def test_task_post(self):
        
        u=User.objects.create(username="nirmal",password="password")
        # data=mixer.blend(Task,member=u)
        # print(data.member)
        data = {
            "task": "devops",
            "member": u.username,  # Use user's primary key instead of object
            "due_date": "2024-03-18"
        }
        
        response=self.client.post(reverse("addtask"),data)
        print(response)
        self.assertAlmostEqual(response.status_code,200)
        self.assertAlmostEqual(Task.objects.get(member__username="nirmal").task,"devops")
        # self.assertAlmostEqual(Task.objects.get(member__username="nirmal").member_id,1)
        
    def test_task_delete(self):
        u=User.objects.create(username="nirmal",password="password")
        # task=Task.objects.create(task="devops",member_id=u.id,due_date="2024-03-18")
        m=mixer.blend(Task,member_id=u.id)
     
        data=json.dumps({"id":1})
        
        response=self.client.delete(reverse("deletetask",args=[1]),data)
        print(response)
        self.assertAlmostEqual(response.status_code,204)
            
        
        
        
        
                        
    
    