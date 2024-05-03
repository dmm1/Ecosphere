# apps/organization/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from .models import User, Country, CountryAdmin, Group, Team
from django.utils.translation import gettext_lazy as _
from django.forms.models import ModelChoiceField



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

class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.all()
        self.fields['country'].required = True


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name} - {obj.email} ({obj.countryadmin.country.name})"

class TeamUpdateForm(forms.ModelForm):
    users = UserModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label=_("Users"),
        widget=forms.CheckboxSelectMultiple,
        to_field_name='id',
    )

    class Meta:
        model = Team
        fields = ['name', 'description', 'group', 'country', 'users']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TeamUpdateForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['group'].queryset = Group.objects.filter(created_by=user)
            if hasattr(user, 'countryadmin'):
                self.fields['country'].queryset = Country.objects.filter(id=user.countryadmin.country.id)
            else:
                self.fields['country'].queryset = Country.objects.all()
            self.fields['users'].queryset = get_user_model().objects.filter(groups__in=user.groups.all())

    def save(self, commit=True):
        team = super().save(commit=False)
        team.save()
        team.users.set(self.cleaned_data['users'])
        return team
