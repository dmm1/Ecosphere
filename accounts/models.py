from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    forename = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(blank=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_images', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.forename = self.user.first_name
        self.surname = self.user.last_name
        self.email_address = self.user.email
        super(UserProfile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('accounts:profile')
    else:
        return redirect('accounts:profile')
# Create your models here.
