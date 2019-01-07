from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from qumed.constants import CHAR_LENGTH_32


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=CHAR_LENGTH_32, null=False, blank=False)
    last_name = models.CharField(max_length=CHAR_LENGTH_32, null=False, blank=False)
    telephone = PhoneNumberField(null=True, blank=True)
    practice = models.ForeignKey('referral.Practice',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
