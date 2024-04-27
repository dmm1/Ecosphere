from django import forms
from django.contrib.auth.models import User
from .models import Contact
from django.core.validators import EmailValidator

class ContactForm(forms.ModelForm):
    assign_to_me = forms.BooleanField(required=False)
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'academic_title', 'email', 'phone', 'title', 'department', 'business_partner', 'address', 'notes', 'last_contacted', 'preferred_communication', 'user', 'assign_to_me']
