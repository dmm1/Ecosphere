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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')

    def get_full_address(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.postcode}, {self.country}"

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
# Create your models here
class Contact(models.Model):
    TITLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Director', 'Director'),
        ('Executive', 'Executive'),
        ('Other', 'Other'),
    ]

    JOB_FUNCTION_CHOICES = [
        ('Sales', 'Sales'),
        ('Marketing', 'Marketing'),
        ('IT', 'IT'),
        ('Finance', 'Finance'),
        ('HR', 'HR'),
        ('Other', 'Other'),
    ]

    PREFERRED_COMMUNICATION_CHOICES = [
        ('Email', 'Email'),
        ('Phone', 'Phone'),
        ('Text', 'Text'),
        ('In-Person', 'In-Person'),
    ]

    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    academic_title = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES)
    job_function = models.CharField(max_length=50, choices=JOB_FUNCTION_CHOICES)
    business_partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    preferred_communication = models.CharField(max_length=50, choices=PREFERRED_COMMUNICATION_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.academic_title:
            return f"{self.academic_title} {self.first_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def get_address(self):
        if self.business_partner:
            return self.business_partner.address
        else:
            return self.address

LEAD_STATUS_CHOICES = [
    ('New', 'New'),
    ('Open', 'Open'),
    ('Contacted', 'Contacted'),
    ('Qualified', 'Qualified'),
    ('Won', 'Won'),
    ('Lost', 'Lost'),
]

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    business_partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, related_name='leads', blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='leads', blank=True, null=True)
    status = models.CharField(max_length=50, choices=LEAD_STATUS_CHOICES, default='New')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
