from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    TITLE_CHOICES = [
        ('Manager', _('Manager')),
        ('Director', _('Director')),
        ('Executive', _('Executive')),
        ('Other', _('Other')),
    ]

    DEPARTMENT_CHOICES = [
        ('Sales', _('Sales')),
        ('Marketing', _('Marketing')),
        ('IT', _('IT')),
        ('Finance', _('Finance')),
        ('HR', _('HR')),
        ('Other', _('Other')),
    ]

    PREFERRED_COMMUNICATION_CHOICES = [
        ('Email', _('Email')),
        ('Phone', _('Phone')),
        ('Text', _('Text')),
        ('In-Person', _('In-Person')),
    ]

    first_name = models.CharField(max_length=50, default='', db_index=True)
    last_name = models.CharField(max_length=50, default='', db_index=True)
    academic_title = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    business_partner = models.ForeignKey('business_partner.BusinessPartner', on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    last_contacted = models.DateField(default=date.today)
    preferred_communication = models.CharField(max_length=50, choices=PREFERRED_COMMUNICATION_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

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
