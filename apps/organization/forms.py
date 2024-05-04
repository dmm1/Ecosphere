# apps/organization/forms.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission, Group as AuthGroup
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.forms.models import ModelChoiceField
from django.forms.widgets import SelectMultiple
from django.forms.widgets import Select
from django_select2.forms import ModelSelect2MultipleWidget
from django.urls import reverse_lazy
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
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ['name', 'description', 'country', 'permissions']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if hasattr(user, 'countryadmin'):
            self.fields['country'].queryset = Country.objects.filter(id=user.countryadmin.country.id)
        else:
            self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True
        self.fields['permissions'].queryset = Permission.objects.all()

    def save(self, commit=True):
        group = super().save(commit=False)
        group.created_by = self.user
        if commit:
            group.save()
            group.permissions.set(self.cleaned_data['permissions'])
        return group

class GroupUpdateForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ['name', 'description', 'country', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True
        self.fields['permissions'].queryset = Permission.objects.all()

import logging
logger = logging.getLogger(__name__)
from django import forms
from .models import Team
from .models import Group, Country

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'group', 'country', 'created_by']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TeamForm, self).__init__(*args, **kwargs)

        if user:
            print(f"User: {user}")
            self.fields['group'].queryset = Group.objects.filter(created_by=user)
            if hasattr(user, 'countryadmin'):
                print(f"User is a country admin for {user.countryadmin.country}")
                self.fields['country'].queryset = Country.objects.filter(id=user.countryadmin.country.id)
            else:
                print("User is not a country admin")
                self.fields['country'].queryset = Country.objects.all()
            self.fields['country'].required = True
            self.fields['created_by'].initial = user

    def save(self, commit=True):
        team = super().save(commit=False)
        print(f"Saving team: {team}")

        if commit:
            team.save()
        return team



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    widget = SelectMultiple(
        attrs={
            'class': 'form-control select2',
            'data-ajax--url': reverse_lazy('organization:user_autocomplete'),
            'data-ajax--cache': 'true',
            'data-ajax--dataType': 'json',
            'data-ajax--delay': 250,
            'data-minimum-input-length': 1,
            'style': 'width: 100%;',
        }
    )

    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name} - {obj.email} ({obj.countryadmin.country.name})"

class RemoveMembersField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        return self.queryset.filter(id__in=value)

class TeamUpdateForm(forms.ModelForm):
    remove_members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label=_("Remove Members"),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }
        )
    )

    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label=_("Members"),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Team
        fields = ['name', 'description', 'group', 'country', 'members', 'remove_members']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TeamUpdateForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['group'].queryset = Group.objects.filter(created_by=self.user)
            if hasattr(self.user, 'countryadmin'):
                self.fields['country'].queryset = Country.objects.filter(id=self.user.countryadmin.country.id)
            else:
                self.fields['country'].queryset = Country.objects.all()
            self.fields['country'].required = True

            # Preselect the current team members
            self.fields['members'].initial = self.instance.members.all()
            self.fields['remove_members'].initial = []

        # Apply Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        team = super().save(commit=False)

        # Remove the selected members from the team
        for member in self.cleaned_data['remove_members']:
            team.members.remove(member)

        # Add the new members to the team
        for member in self.cleaned_data['members']:
            if member not in team.members.all():
                team.members.add(member)

        if commit:
            team.save()
        return team


