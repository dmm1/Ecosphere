# Generated by Django 5.0.4 on 2024-05-18 19:46

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business_partner', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('academic_title', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('title', models.CharField(blank=True, choices=[('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('Other', 'Other')], max_length=50, null=True)),
                ('department', models.CharField(blank=True, choices=[('Sales', 'Sales'), ('Marketing', 'Marketing'), ('IT', 'IT'), ('Finance', 'Finance'), ('HR', 'HR'), ('Other', 'Other')], max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('last_contacted', models.DateField(default=datetime.date.today)),
                ('preferred_communication', models.CharField(blank=True, choices=[('Email', 'Email'), ('Phone', 'Phone'), ('Text', 'Text'), ('In-Person', 'In-Person')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='business_partner.businesspartner')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
