from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Priority(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    # category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE,default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.title
    
class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit from {self.ip_address}"