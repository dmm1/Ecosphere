# Generated by Django 5.0.4 on 2024-04-29 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_partner', '0003_businesspartner_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businesspartner',
            old_name='countries',
            new_name='country',
        ),
    ]
