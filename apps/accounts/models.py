from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_images', null=True, blank=True)

    def __str__(self):
        return self.user.username
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not UserProfile.objects.filter(user=instance).exists():
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

