from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class BusinessPartner(models.Model):
    INDUSTRY_CHOICES = [
        ('Manufacturing', _('Manufacturing')),
        ('Retail', _('Retail')),
        ('Healthcare', _('Healthcare')),
        ('Technology', _('Technology')),
        ('Finance', _('Finance')),
        ('Education', _('Education')),
        ('Construction', _('Construction')),
        ('Transportation', _('Transportation')),
        ('Agriculture', _('Agriculture')),
        ('Energy', _('Energy')),
    ]
    
    PRIMARY_ROLE_CHOICES = [
        ('customer', _('Customer')),
        ('merchant', _('Merchant')),
        ('partner', _('Partner')),
    ]
    
    SECONDARY_ROLE_CHOICES = [
        ('customer', _('Customer')),
        ('merchant', _('Merchant')),
        ('partner', _('Partner')),
        ('-', _('-')),
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
    industry = models.CharField(max_length=200, choices=INDUSTRY_CHOICES, default=INDUSTRY_CHOICES[0][0])
    primary_role = models.CharField(max_length=100, choices=PRIMARY_ROLE_CHOICES, default=PRIMARY_ROLE_CHOICES[0][0])
    secondary_role = models.CharField(max_length=100, choices=SECONDARY_ROLE_CHOICES, default=SECONDARY_ROLE_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers', null=True)
    contact = models.ForeignKey('contact.Contact', on_delete=models.SET_NULL, null=True, blank=True)

    def get_full_address(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.postcode}, {self.country}"

    def __str__(self):
        return self.name