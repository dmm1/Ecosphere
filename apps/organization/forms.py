# apps/organization/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from .models import User, Country, CountryAdmin, Group, Team




class UserCreationForm(DjangoUserCreationForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=True, empty_label=None)

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'country']

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if hasattr(self.user, 'countryadmin'):
            self.fields['country'].initial = self.user.countryadmin.country
            self.fields['country'].widget = forms.HiddenInput()
        else:
            self.fields['country'].queryset = Country.objects.all()
            self.fields['country'].empty_label = '--- Select a country ---'

    def save(self, commit=True):
        user = super().save(commit=False)
        if hasattr(self.user, 'countryadmin'):
            country_admin = CountryAdmin(user=user, country=self.user.countryadmin.country)
            if commit:
                user.save()
                country_admin.save()
        elif 'country' in self.cleaned_data:
            country_admin = CountryAdmin(user=user, country=self.cleaned_data['country'])
            if commit:
                user.save()
                country_admin.save()
        return user

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
        fields = ['name', 'description', 'group', 'country','created_by']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if hasattr(user, 'countryadmin'):
            self.fields['country'].queryset = Country.objects.filter(id=user.countryadmin.country.id)
        else:
            self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True

    def save(self, commit=True):
        team = super().save(commit=False)
        team.created_by = self.user
        if commit:
            team.save()
        return team

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
        fields = ['name', 'description', 'group', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all()
        self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True
