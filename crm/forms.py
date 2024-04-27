from django import forms
from django.contrib.auth.models import User
from .models import Opportunity,  Lead
from django.core.validators import EmailValidator

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'customer', 'amount', 'probability', 'status']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'business_partner', 'contact', 'status', 'notes']
