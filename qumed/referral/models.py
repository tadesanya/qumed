import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from qumed.constants import char_length_16, char_length_32, char_length_128, APPOINTMENT_STATUS


class Practice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=char_length_32, unique=True)
    address = models.CharField(max_length=char_length_128)
    email = models.EmailField()
    telephone = PhoneNumberField()


class Patient(models.Model):
    mrn = models.IntegerField(unique=True)
    name = models.CharField(max_length=char_length_32, unique=True)
    address = models.CharField(max_length=char_length_128)
    email = models.EmailField()
    telephone = PhoneNumberField()


class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=char_length_16, choices=APPOINTMENT_STATUS)
    notes = models.TextField()

    date_referred = models.DateField(auto_now_add=True)
    referred_by = models.ForeignKey(Practice,
                                    on_delete=models.CASCADE,
                                    related_name='outgoing_referrals')
    referred_to = models.ForeignKey(Practice,
                                    on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True,
                                    related_name='incoming_referrals')
    reason_for_referral = models.CharField(max_length=char_length_128)

    first_attempt = models.DateTimeField(null=True, blank=True)
    second_attempt = models.DateTimeField(null=True, blank=True)
    third_attempt = models.DateTimeField(null=True, blank=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
