from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Employee, Department, Position

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class EmployeeForm(forms.ModelForm):
    description = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Employee
        fields = ['user', 'department', 'position', 'description']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['description'].initial = self.instance.position.description
            self.fields['description'].disabled = True

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'description']            