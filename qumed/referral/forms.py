from django.forms import modelform_factory
from django import forms

from .models import Practice, Patient, Referral, TempReferral, Appointment
from qumed.constants import REFERRAL_STATUS, APPOINTMENT_STATUS


# model forms
PracticeForm = modelform_factory(Practice, fields=('name', 'address', 'email', 'telephone'))
PatientForm = modelform_factory(Patient, fields=('mrn', 'name', 'address', 'email', 'telephone'))
ReferralForm = modelform_factory(Referral, fields=('patient', 'notes', 'referred_by',
                                                   'referred_to', 'reason_for_referral'))
TempReferralForm = modelform_factory(TempReferral, exclude=())
AppointmentForm = modelform_factory(Appointment, fields=('appointment_status', 'first_attempt', 'second_attempt',
                                                         'third_attempt', 'appointment_date'))


# non model forms
class AcceptRejectForm(forms.Form):
    referral_id = forms.UUIDField()
    referral_status = forms.ChoiceField(choices=REFERRAL_STATUS, widget=forms.HiddenInput)


class AppointmentCreateForm(forms.Form):
    patient = forms.CharField(widget=forms.HiddenInput())
    practice = forms.CharField(widget=forms.HiddenInput())
    appointment_status = forms.ChoiceField(choices=APPOINTMENT_STATUS)

    first_attempt = forms.CharField()
    second_attempt = forms.CharField()
    third_attempt = forms.CharField()
    appointment_date = forms.CharField()
