import os
from django.conf import settings
import json
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Load the currencies from the JSON file
json_file_path = os.path.join(settings.BASE_DIR, 'static', 'settings', 'currency.json')
with open(json_file_path) as f:
    CURRENCIES = [(currency['code'], currency['name']) for currency in json.load(f)]

# Load the timezones from the JSON file
json_file_path = os.path.join(settings.BASE_DIR, 'static', 'settings', 'timezones.json')
with open(json_file_path) as f:
    TIMEZONES = [(timezone['code'], timezone['name']) for timezone in json.load(f)]

# Load the languages from the JSON file
json_file_path = os.path.join(settings.BASE_DIR, 'static', 'settings', 'languages.json')
with open(json_file_path) as f:
    LANGUAGES = [(language['code'], language['name']) for language in json.load(f)]

class CountrySetting(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='settings')
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    timezone = models.CharField(max_length=50, choices=TIMEZONES)
    language = models.CharField(max_length=50, choices=LANGUAGES)

    def __str__(self):
        return f"Settings for {self.country.name}"
    
class CountryAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='countryadmin')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.country.name})"

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None, null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='organization_group_permissions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return self.name
