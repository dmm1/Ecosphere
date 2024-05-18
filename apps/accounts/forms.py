from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    country = forms.ChoiceField(choices=UserProfile.COUNTRIES_CHOICES, required=True)
    language = forms.ChoiceField(choices=UserProfile.LANGUAGES_CHOICES, required=True)
    timezone = forms.ChoiceField(choices=UserProfile.TIMEZONES_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = ('bio', 'phone_number', 'country', 'language', 'timezone')  # removed 'profile_picture'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['bio'].initial = user.profile.bio
            self.fields['phone_number'].initial = user.profile.phone_number
            self.fields['country'].initial = user.profile.country
            self.fields['language'].initial = user.profile.language
            self.fields['timezone'].initial = user.profile.timezone