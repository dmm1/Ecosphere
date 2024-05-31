# tasks/models.py
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('todo', _('To Do')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    title = models.CharField(max_length=100, default='New Task')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='todo')
    completed = models.BooleanField(default=False)
    due_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user} on {self.task}'