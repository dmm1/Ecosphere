from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bid = models.IntegerField(default=00000)
    name = models.CharField(max_length=100)
    date_of_creation = models.DateField()
    Potential = models.IntegerField()
    users = models.ManyToManyField(User, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()