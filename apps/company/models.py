from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.utils import timezone

def country_choices():
    UserProfile = apps.get_model('accounts', 'UserProfile')
    return UserProfile.COUNTRIES_CHOICES

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=2, choices=country_choices, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)    
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    street_number = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Team(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    members = models.ManyToManyField('Employee', related_name='teams')

    def __str__(self):
        return self.title

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.username} - {self.department.name} - {self.position.title} - {self.position.description}"
    

