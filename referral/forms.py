from django.forms import modelform_factory
from django import forms

from .models import Practice, Patient, Referral, TempReferral, Appointment
from qumed.constants import REFERRAL_STATUS, APPOINTMENT_STATUS


# model forms
PracticeForm = modelform_factory(Practice, fields=('name', 'address', 'city', 'state', 'zipcode', 'email', 'telephone'))
ReferralForm = modelform_factory(Referral, fields=('patient', 'notes', 'referred_by',
                                                   'referred_to', 'reason_for_referral'))
TempReferralForm = modelform_factory(TempReferral, exclude=())


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['mrn', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'telephone', 'dob']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['dob'].id_for_label)
        })


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_status', 'first_attempt', 'second_attempt', 'third_attempt', 'appointment_date']

    def __init__(self,  *args, **kwargs):
        super(AppointmentForm, self).__init__( *args, **kwargs)
        self.fields['first_attempt'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['first_attempt'].id_for_label)
        })

        self.fields['second_attempt'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['second_attempt'].id_for_label)
        })

        self.fields['third_attempt'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['third_attempt'].id_for_label)
        })

        self.fields['appointment_date'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['appointment_date'].id_for_label)
        })


# non model forms
class AcceptRejectForm(forms.Form):
    referral_id = forms.UUIDField()
    referral_status = forms.ChoiceField(choices=REFERRAL_STATUS, widget=forms.HiddenInput)


class AppointmentCreateForm(forms.Form):
    patient = forms.CharField(widget=forms.HiddenInput())
    practice = forms.CharField(widget=forms.HiddenInput())
    appointment_status = forms.ChoiceField(choices=APPOINTMENT_STATUS)

    first_attempt = forms.DateTimeField(required=True)
    second_attempt = forms.DateTimeField(required=False)
    third_attempt = forms.DateTimeField(required=False)
    appointment_date = forms.DateTimeField(required=False)

    def __init__(self,  *args, **kwargs):
        super(AppointmentForm, self).__init__( *args, **kwargs)
        self.fields['first_attempt'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['first_attempt'].id_for_label)
        })

        self.fields['second_attempt'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['second_attempt'].id_for_label)
        })

        self.fields['third_attempt'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['third_attempt'].id_for_label)
        })

        self.fields['appointment_date'].widget.attrs.update({
            'class': 'datetimepicker-input',
            'autocomplete': 'off',
            'data-toggle': 'datetimepicker',
            'data-target': '#{}'.format(self['appointment_date'].id_for_label)
        })
