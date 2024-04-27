from django.core.management.base import BaseCommand
from apps.contact.models import Contact
from apps.business_partner.models import BusinessPartner
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with Contact instances'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **kwargs):
        for i in range(10):  # Change the range to the number of instances you want to create
            contact_data = self.generate_fake_data(Contact)
            contact_data['business_partner'] = BusinessPartner.objects.first() if BusinessPartner.objects.exists() else None
            contact, created = Contact.objects.get_or_create(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                defaults=contact_data
            )

            if not created:
                for key, value in contact_data.items():
                    setattr(contact, key, value)
                contact.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded Contact instances'))

    def generate_fake_data(self, model):
        data = {}
        for field in model._meta.get_fields():
            if field.name in ['id', 'created_at', 'updated_at']:
                continue
            elif field.get_internal_type() == 'CharField':
                data[field.name] = self.faker.word()
            elif field.get_internal_type() == 'TextField':
                data[field.name] = self.faker.text()
            elif field.get_internal_type() == 'BooleanField':
                data[field.name] = self.faker.boolean()
            elif field.get_internal_type() == 'DateField':
                data[field.name] = self.faker.date()
            # Add more elif conditions here for other field types as needed
        return data