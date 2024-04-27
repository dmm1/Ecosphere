from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.tasks.models import Task, Comment
from django.utils import timezone
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        self.run()

    def run(self):
        for _ in range(10):
            # Create a user
            user = User.objects.create_user(username=self.fake.user_name(), password=self.fake.password())

            # Create a task
            task_data = self.generate_fake_data(Task)
            task_data['assigned_to'] = user
            task = Task.objects.create(**task_data)

            # Create a comment
            comment_data = self.generate_fake_data(Comment)
            comment_data['task'] = task
            comment_data['user'] = user
            Comment.objects.create(**comment_data)

    def generate_fake_data(self, model):
        data = {}
        for field in model._meta.get_fields():
            if field.name in ['id', 'created_at', 'updated_at']:
                continue
            elif field.get_internal_type() == 'CharField':
                data[field.name] = self.fake.word()
            elif field.get_internal_type() == 'TextField':
                data[field.name] = self.fake.text()
            elif field.get_internal_type() == 'BooleanField':
                data[field.name] = self.fake.boolean()
            elif field.get_internal_type() == 'DateField':
                data[field.name] = self.fake.date()
            # Add more elif conditions here for other field types as needed
        return data