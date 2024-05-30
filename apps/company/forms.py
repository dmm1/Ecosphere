from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Employee, Department, Position

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class EmployeeForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    description = forms.CharField(max_length=100, required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\+\d+$', phone_number):
            raise ValidationError('Phone number must start with + followed by digits.')
        return phone_number
    
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user']  # Exclude the user field
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['user'].initial = self.instance.user
            self.fields['description'].initial = self.instance.position.description
            self.fields['description'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.user = self.cleaned_data['user']
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