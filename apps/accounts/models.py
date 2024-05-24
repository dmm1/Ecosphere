from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pytz
from apps.company.models import Employee

class UserProfile(models.Model):
    COUNTRIES_CHOICES = (
        ('US', 'United States'),
        ('AT', 'Austria'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('ES', 'Spain'),
        ('IT', 'Italy'),
        ('JP', 'Japan'),
        ('CN', 'China'),
        ('IN', 'India'),
        ('BR', 'Brazil'),
    )

    LANGUAGES_CHOICES = (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('it', 'Italian'),
        ('jp', 'Japanese'),
        ('cn', 'Chinese'),
        ('hi', 'Hindi'),
        ('pt', 'Portuguese'),
    )

    TIMEZONES_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_images', null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES_CHOICES, default='US', null=False)
    language = models.CharField(max_length=2, choices=LANGUAGES_CHOICES, default='en')
    timezone = models.CharField(max_length=32, choices=TIMEZONES_CHOICES, default='UTC')

    def __str__(self):
        return self.user.username