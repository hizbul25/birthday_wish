from datetime import datetime, timedelta
from random import randint

from dateutil.relativedelta import relativedelta
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
            dob = fake.date_of_birth(minimum_age=20, maximum_age=50)

            dob_datetime = timezone.datetime.combine(dob, datetime.min.time())

            today_datetime = timezone.datetime.combine(
                today, datetime.min.time())
            if (dob_datetime - today_datetime).days < 0:
                dob_datetime = today_datetime + timedelta(days=randint(0, 5))

            if (dob_datetime.date() - today).days <= 5:
                customers.append(Customer(
                    name=fake.name(),
                    address=fake.address(),
                    email=fake.email(),
                    dob=dob_datetime.date()
                ))

        return customers
