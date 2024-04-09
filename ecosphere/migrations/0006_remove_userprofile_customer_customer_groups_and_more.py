# Generated by Django 5.0.4 on 2024-04-09 21:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ecosphere', '0005_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='customer',
        ),
        migrations.AddField(
            model_name='customer',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
        migrations.AddField(
            model_name='customer',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]