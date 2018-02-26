from django.forms import modelform_factory

from .models import Practice, Patient, Referral


PracticeForm = modelform_factory(Practice, fields=('name', 'address', 'email', 'telephone'))
PatientForm = modelform_factory(Patient, fields=('mrn', 'name', 'address', 'email', 'telephone'))
Referral = modelform_factory(Referral, fields=('patient', 'status', 'notes', 'date_referred', 'referred_by',
                                               'referred_to', 'reason_for_referral', 'first_attempt', 'second_attempt',
                                               'third_attempt', 'appointment_date'))
