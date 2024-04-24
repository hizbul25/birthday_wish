
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from common.helper import convert_to_human_readable
from customer.tasks import send_customer_birthday_message


class Command(BaseCommand):
    help = 'Add a customer with optional birthday parameter'

    def add_arguments(self, parser):
        parser.add_argument('--dob', type=str, nargs='?',
                            default=timezone.now().strftime('%m-%d'), help='Customer birthday (MM-DD)')

    def handle(self, *args, **kwargs):
        dob_str = kwargs['dob']
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, '%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    'Invalid date format. Please use MM-DD format.'))
                return
        else:
            dob = timezone.now().date()

        self.stdout.write(self.style.SUCCESS(
            f'Customer birthday: {convert_to_human_readable(dob.day, dob.month)}'))
        send_customer_birthday_message.delay(dob)
