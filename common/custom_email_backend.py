# custom_email_backend.py

import logging

from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)


class LoggingEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            logger.info("Subject: %s\nTo: %s\nFrom: %s\n%s" % (
                message.subject, message.to, message.from_email, message.body))
        return len(email_messages)
