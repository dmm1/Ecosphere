from django.core.management.base import BaseCommand
from apps.contact.models import Contact
from apps.business_partner.models import BusinessPartner
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with Contact instances'

    def handle(self, *args, **options):
        faker = Faker()
        titles = ['Manager', 'Director', 'Executive', 'Other']
        departments = ['Sales', 'Marketing', 'IT', 'Finance', 'HR', 'Other']
        communications = ['Email', 'Phone', 'Text', 'In-Person']

        for i in range(10):  # Change the range to the number of instances you want to create
            contact, created = Contact.objects.get_or_create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                defaults={
                    'academic_title': faker.job(),
                    'email': faker.email(),
                    'phone': faker.phone_number()[:20],
                    'title': faker.random_element(elements=titles),
                    'department': faker.random_element(elements=departments),
                    'notes': faker.text(),
                    'preferred_communication': faker.random_element(elements=communications),
                    # Add a valid user instance
                    'business_partner': BusinessPartner.objects.first() if BusinessPartner.objects.exists() else None
                }
            )

            if not created:
                contact.academic_title = faker.job()
                contact.email = faker.email()
                contact.phone = faker.phone_number()
                contact.title = faker.random_element(elements=titles)
                contact.department = faker.random_element(elements=departments)
                contact.notes = faker.text()
                contact.preferred_communication = faker.random_element(elements=communications)
                contact.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded Contact instances'))