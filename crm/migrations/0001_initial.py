# Generated by Django 5.0.4 on 2024-04-17 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from crm.models import BusinessPartner

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('primary_role', models.CharField(blank=True, default='Customer', max_length=100, null=True, verbose_name='Primary Role')),
                ('secondary_role', models.CharField(blank=True, default='Merchant', max_length=100, null=True, verbose_name='Secondary Role')),
                ('industry', models.CharField(choices=[('Manufacturing', 'Manufacturing'), ('Retail', 'Retail'), ('Healthcare', 'Healthcare'), ('Technology', 'Technology'), ('Finance', 'Finance'), ('Education', 'Education'), ('Construction', 'Construction'), ('Transportation', 'Transportation'), ('Agriculture', 'Agriculture'), ('Energy', 'Energy')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('probability', models.IntegerField(default=50)),
                ('status', models.CharField(choices=[('open', 'Open'), ('won', 'Won'), ('lost', 'Lost')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='crm.customer')),
            ],
        ),
    ]
