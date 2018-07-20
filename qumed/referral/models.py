import uuid
from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from qumed.constants import CHAR_LENGTH_16, CHAR_LENGTH_32, CHAR_LENGTH_128, APPOINTMENT_STATUS, REFERRAL_STATUS


class Practice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=CHAR_LENGTH_32, unique=True)
    address = models.CharField('Address', max_length=CHAR_LENGTH_128)
    email = models.EmailField('Email')
    telephone = PhoneNumberField('Telephone')
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.CASCADE,
                                   related_name='creator',
                                   editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Patient(models.Model):
    mrn = models.IntegerField('Medical Record Number', unique=True)
    name = models.CharField('Name', max_length=CHAR_LENGTH_32, unique=True)
    address = models.CharField('Address', max_length=CHAR_LENGTH_128)
    email = models.EmailField('Email')
    telephone = PhoneNumberField('Telephone')

    creator_practice = models.ForeignKey(Practice,
                                         on_delete=models.CASCADE,
                                         related_name='created_patients',
                                         editable=False)
    current_practice = models.ForeignKey(Practice,
                                         on_delete=models.CASCADE,
                                         related_name='current_patients')

    def __str__(self):
        return "{} ({})".format(self.name, self.mrn)

    class Meta:
        ordering = ["name"]


class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    notes = models.TextField('Notes')
    date_referred = models.DateField(default=date.today, editable=False)
    reason_for_referral = models.CharField('Reason for referral', max_length=CHAR_LENGTH_128)
    referral_status = models.CharField('Referral Status',
                                       max_length=CHAR_LENGTH_16,
                                       choices=REFERRAL_STATUS,
                                       default='pending')

    referred_by = models.ForeignKey(Practice,
                                    on_delete=models.CASCADE,
                                    related_name='outgoing_referrals')
    referred_to = models.ForeignKey(Practice,
                                    on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True,
                                    related_name='incoming_referrals')

    appointment_status = models.CharField('Appointment Status',
                                          max_length=CHAR_LENGTH_16,
                                          choices=APPOINTMENT_STATUS,
                                          default='lmts')
    first_attempt = models.DateTimeField('First Attempt', null=True, blank=True)
    second_attempt = models.DateTimeField('Second Attempt', null=True, blank=True)
    third_attempt = models.DateTimeField('Third Attempt', null=True, blank=True)
    appointment_date = models.DateTimeField('Appointment Date', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-date_referred"]


class TempReferral(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    notes = models.TextField()
    reason_for_referral = models.CharField(max_length=CHAR_LENGTH_128)
    referred_by = models.ForeignKey(Practice, on_delete=models.CASCADE)
    referred_to_email = models.EmailField('Email')
    date_referred = models.DateField(auto_now_add=True)
