from django.core.management.base import BaseCommand
from django.utils import timezone

from customer.tasks import send_customer_birthday_message


class Command(BaseCommand):
    help = 'send bd wish to customer'
    today = timezone.now().date()

    def add_arguments(self, parser):
        parser.add_argument('--dob', type=int, nargs='?',
                            default=timezone.now().date(), help='Customer birthday')

    def handle(self, *args, **options):
        dob = options['dob']
        send_customer_birthday_message.delay(dob)
