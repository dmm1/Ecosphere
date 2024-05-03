# Generated by Django 5.0.4 on 2024-05-03 07:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
    ]
