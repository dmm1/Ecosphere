from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.translation import gettext_lazy as _

# Forward-declare the Contact model

class Opportunity(models.Model):
    name = models.CharField(max_length=100)
    customer = models.ForeignKey('business_partner.BusinessPartner', on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    probability = models.IntegerField(default=50)
    status = models.CharField(max_length=50, choices=[
        ('open', _('Open')),
        ('won', _('Won')),
        ('lost', _('Lost')),
        ('finished', _('Finished')),
        ('in_progress', _('In Progress')),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

LEAD_STATUS_CHOICES = [
    ('New', _('New')),
    ('Open', _('Open')),
    ('Contacted', _('Contacted')),
    ('Qualified', _('Qualified')),
    ('Won', _('Won')),
    ('Lost', _('Lost')),
]

LEAD_SOURCE_CHOICES = [
    ('Web', _('Web')),
    ('Phone', _('Phone')),
    ('Email', _('Email')),
    ('Other', _('Other')),
]

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    business_partner = models.ForeignKey('business_partner.BusinessPartner', on_delete=models.CASCADE, related_name='leads', blank=True, null=True)
    contact = models.ForeignKey('contact.Contact', on_delete=models.CASCADE, related_name='leads', blank=True, null=True)
    status = models.CharField(max_length=50, choices=LEAD_STATUS_CHOICES, default='New')
    source = models.CharField(max_length=50, choices=LEAD_SOURCE_CHOICES, default='Web')  
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
