import unittest
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from customer.tasks import (schedule_wish_customer_birthday,
                            send_customer_birthday_message)

from .models import Customer


class TestCustomer(unittest.TestCase):
    def setUp(self):
        call_command("makemigrations", verbosity=0)
        call_command("migrate", verbosity=0)
        self.client = APIClient()

    def test_customer_creation(self):
        customer = Customer(name='Nameera Bahar',
                            email='nameera.bahar@gmail.com', dob='2019-09-25')
        customer.save()
        cust = Customer.objects.filter(email='nameera.bahar@gmail.com').first()
        self.assertEqual('Nameera Bahar', cust.name)

    def test_customer_creation_api(self):
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'address': '123 Main St',
            'dob': '1990-01-01'  # Assuming date of birth format is YYYY-MM-DD
        }

        response = self.client.post(
            reverse('customer-register'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Customer.objects.filter(email=data['email']).exists())

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['address'], data['address'])
        self.assertEqual(response.data['dob'], data['dob'])

    def test_customer_list(self):
        cust = Customer.objects.all()
        self.assertEqual(len(cust), 2)


class TestCeleryTasks(unittest.TestCase):

    def setUp(self):
        self.mock_call_command = Mock()
        self.mock_send_mail = Mock()
        self.mock_filter = Mock(return_value=[])

        self.patch_call_command = patch(
            'customer.tasks.call_command', self.mock_call_command)
        self.patch_send_mail = patch(
            'customer.tasks.send_mail', self.mock_send_mail)
        self.patch_filter = patch(
            'customer.tasks.Customer.objects.filter', self.mock_filter)

        self.patch_call_command.start()
        self.patch_send_mail.start()
        self.patch_filter.start()

    def tearDown(self):
        self.patch_call_command.stop()
        self.patch_send_mail.stop()
        self.patch_filter.stop()

    def test_schedule_wish_customer_birthday(self):
        schedule_wish_customer_birthday.apply()
        self.mock_call_command.assert_called_once_with("wish_birthday")

    def test_send_customer_birthday_message(self):
        send_customer_birthday_message.apply(args=[timezone.now().date()])
        self.mock_send_mail.assert_called_once_with(
            "Happy Birthday dear customer!",
            "Dear Sir,\n\nWishing you a fantastic birthday filled with joy and happiness!\n\nBest regards,\nHizbul Bahar, Panthapath, Dhaka",
            'info@bdwisher.com',
            []
        )


if __name__ == '__main__':
    unittest.main()
