from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .models import BusinessPartner
from apps.contact.models import Contact

class BusinessPartnerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    industry = forms.ChoiceField(choices=BusinessPartner.INDUSTRY_CHOICES)
    primary_role = forms.ChoiceField(choices=BusinessPartner.PRIMARY_ROLE_CHOICES)
    secondary_role = forms.ChoiceField(choices=BusinessPartner.SECONDARY_ROLE_CHOICES)
    email = forms.EmailField(validators=[EmailValidator(message='Please enter a valid email address.')])

    class Meta:
        model = BusinessPartner
        fields = ['name', 'name2', 'vat', 'email', 'phone', 'country', 'state', 'postcode', 'city', 'street_name', 'street_number', 'industry', 'primary_role', 'secondary_role', 'user', 'contact']
