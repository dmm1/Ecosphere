from django.core.management.base import BaseCommand
from apps.business_partner.models import BusinessPartner
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with BusinessPartner instances'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **kwargs):
        for i in range(20):  # Change the range to the number of instances you want to create
            business_partner_data = self.generate_fake_data(BusinessPartner)
            business_partner_data['user'] = User.objects.first() if User.objects.exists() else None
            BusinessPartner.objects.create(**business_partner_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with BusinessPartner instances'))

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