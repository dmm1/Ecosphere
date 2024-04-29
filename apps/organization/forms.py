# apps/organization/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Group, Team, Country

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'country']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if hasattr(user, 'countryadmin'):
            self.fields['country'].queryset = Country.objects.filter(id=user.countryadmin.country.id)
        else:
            self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True

    def save(self, commit=True):
        group = super().save(commit=False)
        group.created_by = self.user
        if commit:
            group.save()
        return group

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'group']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True

class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all()
