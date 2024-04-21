from django import forms
from django.contrib.auth.models import User
from .models import Opportunity, BusinessPartner, Contact, Lead

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'customer', 'amount', 'probability', 'status']

class BusinessPartnerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    industry = forms.ChoiceField(choices=BusinessPartner.INDUSTRY_CHOICES)
    primary_role = forms.ChoiceField(choices=BusinessPartner.PRIMARY_ROLE_CHOICES)
    secondary_role = forms.ChoiceField(choices=BusinessPartner.SECONDARY_ROLE_CHOICES)

    class Meta:
        model = BusinessPartner
        fields = ['name', 'name2', 'vat', 'email', 'phone', 'country', 'state', 'postcode', 'city', 'street_name', 'street_number', 'industry', 'primary_role', 'secondary_role', 'user']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'academic_title', 'email', 'phone', 'title', 'department', 'business_partner', 'address', 'notes', 'last_contacted', 'preferred_communication']

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'business_partner', 'contact', 'status', 'notes']