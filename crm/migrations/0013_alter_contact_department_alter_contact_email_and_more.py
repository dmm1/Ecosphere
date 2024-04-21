# Generated by Django 5.0.4 on 2024-04-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_alter_contact_department_alter_contact_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='department',
            field=models.CharField(blank=True, choices=[('Sales', 'Sales'), ('Marketing', 'Marketing'), ('IT', 'IT'), ('Finance', 'Finance'), ('HR', 'HR'), ('Other', 'Other')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='title',
            field=models.CharField(blank=True, choices=[('Manager', 'Manager'), ('Director', 'Director'), ('Executive', 'Executive'), ('Other', 'Other')], max_length=50, null=True),
        ),
    ]