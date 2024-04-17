# Generated by Django 5.0.4 on 2024-04-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='forename',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
