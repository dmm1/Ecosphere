from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class BusinessPartner(models.Model):
    INDUSTRY_CHOICES = [
        ('Manufacturing', 'Manufacturing'),
        ('Retail', 'Retail'),
        ('Healthcare', 'Healthcare'),
        ('Technology', 'Technology'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Construction', 'Construction'),
        ('Transportation', 'Transportation'),
        ('Agriculture', 'Agriculture'),
        ('Energy', 'Energy'),
    ]

    PRIMARY_ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('merchant', 'Merchant'),
        ('partner', 'Partner'),
    ]

    SECONDARY_ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('merchant', 'Merchant'),
        ('partner', 'Partner'),
        ('-', '-'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    primary_role = models.CharField(_("Primary Role"), max_length=100, choices=PRIMARY_ROLE_CHOICES, default='customer')
    secondary_role = models.CharField(_("Secondary Role"), max_length=100, choices=SECONDARY_ROLE_CHOICES, default='merchant')
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    customer = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, related_name='opportunities')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    probability = models.IntegerField(default=50)
    status = models.CharField(max_length=50, choices=[
        ('open', 'Open'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('finished', 'finished'),
        ('in progress', 'in progress'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')

    def __str__(self):
        return self.name
# Create your models here.
