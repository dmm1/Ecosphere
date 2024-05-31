from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pytz
from apps.company.models import Employee, Company
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    COUNTRIES_CHOICES = (
        ('US', _('United States')),
        ('AT', _('Austria')),
        ('DE', _('Germany')),
        ('FR', _('France')),
        ('ES', _('Spain')),
        ('IT', _('Italy')),
        ('JP', _('Japan')),
        ('CN', _('China')),
        ('IN', _('India')),
        ('BR', _('Brazil')),
    )
    
    LANGUAGES_CHOICES = (
        ('en', _('English')),
        ('de', _('German')),
        ('fr', _('French')),
        ('es', _('Spanish')),
        ('it', _('Italian')),
        ('jp', _('Japanese')),
        ('cn', _('Chinese')),
        ('hi', _('Hindi')),
        ('pt', _('Portuguese')),
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