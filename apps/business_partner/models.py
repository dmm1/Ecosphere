from django.db import models
from django.contrib.auth.models import User

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

    name = models.CharField(max_length=100, default='')
    name2 = models.CharField(max_length=100, default='')
    vat = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    postcode = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=100, default='')
    street_name = models.CharField(max_length=200, default='')
    street_number = models.CharField(max_length=20, default='')
    industry = models.CharField(max_length=200, default='')
    primary_role = models.CharField(max_length=100, default='')
    secondary_role = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers', null=True)
    contact = models.ForeignKey('contact.Contact', on_delete=models.SET_NULL, null=True, blank=True)

    def get_full_address(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.postcode}, {self.country}"

    def __str__(self):
        return self.name
