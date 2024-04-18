from django import forms
from .models import Opportunity, BusinessPartner

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'customer', 'amount', 'probability', 'status']

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'customer', 'amount', 'probability', 'status']

class BusinessParnterForm(forms.ModelForm):
    class Meta:
        model = BusinessPartner
        fields = ['name', 'email', 'phone', 'industry', 'primary_role', 'secondary_role']
