# tasks/forms.py
from django import forms
from .models import Task
from datetime import datetime

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'assigned_to']
        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
