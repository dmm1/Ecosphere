# tasks/models.py
from django.db import models
from datetime import date
class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='todo')
    completed = models.BooleanField(default=False)
    due_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
