from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='opportunities')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    probability = models.IntegerField(default=50)
    status = models.CharField(max_length=50, choices=[
        ('open', 'Open'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')

    def __str__(self):
        return self.name
# Create your models here.
