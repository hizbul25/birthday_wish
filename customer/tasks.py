from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.core.management import call_command

from .models import Customer

logger = get_task_logger(__name__)


@shared_task
def schedule_wish_customer_birthday():
    call_command("wish_birthday", )


@shared_task
def send_customer_birthday_message(dob):
    customers = Customer.objects.filter(dob__month=dob.month, dob__day=dob.day)
    subject = f"Happy Birthday dear customer!"
    message = f"Dear Sir,\n\nWishing you a fantastic birthday filled with joy and happiness!\n\nBest regards,\nHizbul Bahar, Panthapath, Dhaka"
    recipients = [customer.email for customer in customers]
    try:
        send_mail(subject, message, 'info@bdwisher.com', recipients)
        logger.info(
            f"\n\nSuccessfully sent birthday email to all customers with dob {dob}.")
    except Exception as e:
        logger.error(
            f"Failed to send birthday email to customers with dob {dob}: {e}")
