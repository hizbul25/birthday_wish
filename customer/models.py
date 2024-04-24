from django.db import models

from common.models import TimeStampedModel

# Create your models here.


class Customer(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(db_index=True, blank=False)

    def __str__(self) -> str:
        return self.name
