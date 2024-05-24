from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Employee, Department, Position

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=100, required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\+\d+$', phone_number):
            raise ValidationError('Phone number must start with + followed by digits.')
        return phone_number
    
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['description'].initial = self.instance.position.description
            self.fields['description'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.user.username = self.cleaned_data['username']
            instance.user.email = self.cleaned_data['email']
            instance.user.first_name = self.cleaned_data['first_name']
            instance.user.last_name = self.cleaned_data['last_name']
            instance.user.save()
            instance.save()
        return instance

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'description']            