# Generated by Django 5.0.4 on 2024-04-20 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_assigned_to_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_to_user',
        ),
    ]
