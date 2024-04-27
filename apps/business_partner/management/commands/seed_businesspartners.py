from django.core.management.base import BaseCommand
from apps.business_partner.models import BusinessPartner
from django.contrib.auth.models import User
import random
import faker

class Command(BaseCommand):
    help = 'Seeds the database with BusinessPartner instances'

    def handle(self, *args, **options):
        fake = faker.Faker()

        # List of possible values for the fields
        primary_roles = ['customer', 'merchant', 'partner']
        secondary_roles = ['customer', 'merchant', 'partner', '-']
        industries = ['Manufacturing', 'Retail', 'Healthcare', 'Technology', 'Finance', 'Education', 'Construction', 'Transportation', 'Agriculture', 'Energy']
        users = list(User.objects.all())

        # Create new BusinessPartner instances
        for i in range(20):  # Change this number to the number of instances you want to create
            BusinessPartner.objects.create(
                name=fake.company(),
                name2=fake.company_suffix(),
                vat=fake.random_number(digits=9),
                email=fake.company_email(),
                phone=fake.phone_number()[:15],
                user=random.choice(users) if users else None,
                primary_role=random.choice(primary_roles),
                secondary_role=random.choice(secondary_roles),
                street_name=fake.street_name(),
                street_number=fake.building_number(),
                city=fake.city(),
                state=fake.state(),
                postcode=fake.zipcode(),
                country=fake.country(),
                industry=random.choice(industries)
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with BusinessPartner instances'))