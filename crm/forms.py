from django import forms
from .models import Opportunity, Customer

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'customer', 'amount', 'probability', 'status']

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'customer', 'amount', 'probability', 'status']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'industry', 'primary_role', 'secondary_role']
