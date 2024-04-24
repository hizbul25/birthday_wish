from datetime import timezone
from unittest.mock import Mock

from celery.contrib.pytest import celery_app as celery

from customer.tasks import (schedule_wish_customer_birthday,
                            send_customer_birthday_message)


def test_schedule_wish_customer_birthday(celery_worker):
    mock_call_command = Mock()
    schedule_wish_customer_birthday.call_command = mock_call_command
    schedule_wish_customer_birthday.apply()
    mock_call_command.assert_called_once_with("wish_birthday")


def test_send_customer_birthday_message(celery_worker, monkeypatch):
    mock_send_mail = Mock()
    monkeypatch.setattr('customer.tasks.send_mail', mock_send_mail)
    mock_filter = Mock(return_value=[])
    monkeypatch.setattr('customer.tasks.Customer.objects.filter', mock_filter)
    send_customer_birthday_message.apply(args=[timezone.now().date()])
    mock_send_mail.assert_called_once_with(
        "Happy Birthday dear customer!",
        "Dear Sir,\n\nWishing you a fantastic birthday filled with joy and happiness!\n\nBest regards,\nHizbul Bahar, Panthapath, Dhaka",
        'info@bdwisher.com',
        []
    )
