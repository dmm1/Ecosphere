# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
