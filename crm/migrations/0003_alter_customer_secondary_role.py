# Generated by Django 5.0.4 on 2024-04-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_customer_primary_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='secondary_role',
            field=models.CharField(choices=[('customer', 'Customer'), ('merchant', 'Merchant'), ('partner', 'Partner'), ('-', '-')], default='merchant', max_length=100, verbose_name='Secondary Role'),
        ),
    ]
