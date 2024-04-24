from datetime import datetime, timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from customer.models import Customer

fake = Faker()


class Command(BaseCommand):
    help = 'Seed customer with random data'

    def add_arguments(self, parser):
        parser.add_argument('--num_entries', type=int, nargs='?',
                            default=100, help='Number of entries to seed')
        parser.add_argument('--overwrite', action='store_true',
                            help='Overwrite existing customers')

    def handle(self, *args, **options):
        num_entries = options['num_entries']
        overwrite = options['overwrite']

        if overwrite:
            self.stdout.write(self.style.WARNING("Overwriting customers"))
            Customer.objects.all().delete()

        Customer.objects.bulk_create(
            Command.generate_fake_customers(num_entries))

        self.stdout.write(self.style.SUCCESS(
            f'{num_entries} customers added'))

    @staticmethod
    def generate_fake_customers(num_entries: int) -> list:
        fake = Faker()

        customers = []
        today = timezone.now().date()
        for _ in range(num_entries):
            # Generate a random age between 30 and 35
            age_days = randint(30*365, 35*365)
            dob = today - timedelta(days=age_days)

            # Ensure the birthday is within the next 7 days
            birthday = dob.replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)

            # Add customer if birthday is within next 7 days
            if (birthday - today).days <= 7:
                customers.append(Customer(
                    name=fake.name(),
                    address=fake.sentence(),
                    email=fake.email(),
                    dob=birthday
                ))
        return customers
