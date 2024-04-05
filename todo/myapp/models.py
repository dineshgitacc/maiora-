from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    task=models.CharField(max_length=100)
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    due_date=models.DateField()
    
    def __str__(self):
        return self.task