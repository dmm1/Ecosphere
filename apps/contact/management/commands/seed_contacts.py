from django.core.management.base import BaseCommand
from apps.contact.models import Contact
from apps.business_partner.models import BusinessPartner
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with Contact instances'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **kwargs):
        business_partners = list(BusinessPartner.objects.all())
        users = list(User.objects.all())
        for i in range(20):  # Change the range to the number of instances you want to create
            contact_data = self.generate_fake_data(Contact)
            contact_data['business_partner'] = self.faker.random_element(business_partners) if business_partners else None
            contact_data['user'] = self.faker.random_element(users) if users else None
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
                if field.name == 'email':
                    data[field.name] = self.faker.email()
                elif field.name == 'phone':
                    data[field.name] = '+4366555' + str(self.faker.random_int(min=10, max=99))  # Generate phone number in the format +436655588
                elif field.name in ['title', 'department', 'preferred_communication']:
                    data[field.name] = self.faker.random_element(elements=[choice[0] for choice in field.choices])
                else:
                    data[field.name] = self.faker.word()
            elif field.get_internal_type() == 'TextField':
                data[field.name] = self.faker.text()
            elif field.get_internal_type() == 'BooleanField':
                data[field.name] = self.faker.boolean()
            elif field.get_internal_type() == 'DateField':
                data[field.name] = self.faker.date_between(start_date='-30y', end_date='today')
            elif field.get_internal_type() == 'ForeignKey':
                if field.name == 'business_partner':
                    if BusinessPartner.objects.exists():
                        data[field.name] = BusinessPartner.objects.order_by('?').first()
                elif field.name == 'user':
                    if User.objects.exists():
                        data[field.name] = User.objects.order_by('?').first()
            # Add more elif conditions here for other field types as needed
        return data