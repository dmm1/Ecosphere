import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from django.core.management.base import BaseCommand
from apps.business_partner.models import BusinessPartner
from django.contrib.auth.models import User
from apps.contact.models import Contact  # Make sure to adjust the import path according to your project structure
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with BusinessPartner instances and associate contacts'

    def handle(self, *args, **options):
        # Ensure there are at least 2 users
        if User.objects.count() < 2:
            for _ in range(2 - User.objects.count()):
                User.objects.create_user(username=fake.user_name(), email=fake.email())

        # Now that we have at least 2 users, proceed with creating BusinessPartners
        users = User.objects.all()

        # Clear existing entries
        BusinessPartner.objects.all().delete()

        # Seed the database with BusinessPartners
        for _ in range(10):  # Adjust the range to control the number of instances you want to create
            business_partner_data = {
                'name': fake.company(),
                'name2': fake.company(),
                'vat': str(fake.random_int(min=1000, max=9999)) + '%',
                'email': fake.email(),
                'phone': '+4366555' + str(fake.random_int(min=1000, max=9999)),
                'country': fake.country(),
                'state': fake.state(),
                'city': fake.city(),
                'postcode': fake.zipcode(),
                'street_name': fake.street_name(),
                'street_number': str(fake.random_int(min=1, max=999)),
                'industry': fake.random_element(elements=[choice[0] for choice in BusinessPartner.INDUSTRY_CHOICES]),
                'primary_role': fake.random_element(elements=[choice[0] for choice in BusinessPartner.PRIMARY_ROLE_CHOICES]),
                'secondary_role': fake.random_element(elements=[choice[0] for choice in BusinessPartner.SECONDARY_ROLE_CHOICES]),
                'user': fake.random_element(elements=users),
            }
            business_partner = BusinessPartner.objects.create(**business_partner_data)

            # Ensure there are at least 100 associated contacts
            if Contact.objects.filter(business_partner=business_partner).count() < 100:
                for _ in range(100 - Contact.objects.filter(business_partner=business_partner).count()):
                    Contact.objects.create(
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email(),
                        business_partner=business_partner
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database with BusinessPartner instances and associated contacts'))