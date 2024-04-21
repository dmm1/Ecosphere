# Generated by Django 5.0.4 on 2024-04-20 22:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_opportunity_assigned_to_alter_opportunity_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='crm.businesspartner'),
        ),
    ]
