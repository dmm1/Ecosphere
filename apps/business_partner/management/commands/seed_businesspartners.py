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
        users = list(User.objects.all())
        for i in range(20):  # Change the range to the number of instances you want to create
            business_partner_data = self.generate_fake_data(BusinessPartner)
            business_partner_data['user'] = self.faker.random_element(users) if users else None
            BusinessPartner.objects.create(**business_partner_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with BusinessPartner instances'))

    def generate_fake_data(self, model):
        data = {}
        for field in model._meta.get_fields():
            if field.name in ['id', 'created_at', 'updated_at']:
                continue
            elif field.get_internal_type() == 'CharField':
                if field.name == 'email':
                    data[field.name] = self.faker.email()
                elif field.name == 'phone':
                    data[field.name] = '+4366555' + str(self.faker.random_int(min=10, max=99))  # Generate phone number in the format +436655588
                elif field.name in ['industry', 'primary_role', 'secondary_role']:
                    if field.choices is not None:
                        data[field.name] = self.faker.random_element(elements=[choice[0] for choice in field.choices])
                    # Add an else clause here if you want to handle the case where field.choices is None
                elif field.name in ['country', 'state', 'city']:
                    data[field.name] = self.faker.word()
                elif field.name in ['postcode', 'street_number']:
                    data[field.name] = self.faker.random_int(min=1000, max=9999)
                elif field.name == 'street_name':
                    data[field.name] = self.faker.street_name()
                else:
                    data[field.name] = self.faker.word()
            elif field.get_internal_type() == 'EmailField':
                data[field.name] = self.faker.email()
            elif field.get_internal_type() == 'BooleanField':
                data[field.name] = self.faker.boolean()
            elif field.get_internal_type() == 'DateField':
                data[field.name] = self.faker.date_between(start_date='-30y', end_date='today')
            # Add more elif conditions here for other field types as needed
        return data