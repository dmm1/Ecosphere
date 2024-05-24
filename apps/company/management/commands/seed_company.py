# hr/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.company.models import Employee, Department, Position
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with fake data'

    def handle(self, *args, **options):
        fake = Faker()

        # Create fake departments
        for _ in range(5):
            Department.objects.create(name=fake.bs())

        # Create fake positions
        # Create fake positions
        for _ in range(5):
            Position.objects.create(title=fake.job(), description=fake.text(max_nb_chars=100))

        # Create fake users and employees
        # Create fake users and employees
        # Create fake users and employees
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            Employee.objects.create(user=user, department=Department.objects.order_by('?').first(), position=Position.objects.order_by('?').first())
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))