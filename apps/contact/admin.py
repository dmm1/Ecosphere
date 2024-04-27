from django.contrib import admin
from django.contrib.auth.models import User
from .models import Contact

admin.site.register(Contact)
from django.contrib import admin