from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from apps.hr.models import Employee, Position, Department


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
        fields = ['profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')

        try:
            # check file size
            if picture:
                if picture.size > 2*1024*1024:  # 2MB
                    raise ValidationError(_('File size must be at most 1MB.'))

                # check file type
                if not picture.content_type in ['image/jpeg', 'image/png', 'image/webp']:
                    raise ValidationError(_('File type must be .jpg, .png, or .webp.'))

                # check image dimensions
                image = Image.open(BytesIO(picture.read()))
                if image.width < 140:
                    raise ValidationError(_('Image width must be at least 140px.'))

        except AttributeError:
            pass

        return picture

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
            if user.profile.employee:
                self.fields['phone_number'].initial = user.profile.employee.phone_number
            self.fields['country'].initial = user.profile.country
            self.fields['language'].initial = user.profile.language
            self.fields['timezone'].initial = user.profile.timezone