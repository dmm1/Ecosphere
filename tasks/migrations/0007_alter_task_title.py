# Generated by Django 5.0.4 on 2024-04-21 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_task_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='Job Position', max_length=100),
        ),
    ]
