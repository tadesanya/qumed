from django.contrib import admin
from .models import Practice, Patient, Referral, TempReferral, Appointment


class PracticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'telephone', 'created_by')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'mrn', 'name', 'address', 'email', 'telephone', 'creator_practice', 'current_practice')


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date_referred', 'reason_for_referral', 'notes', 'referral_status', 'referred_by',
                    'referred_to')

class TempReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date_referred', 'reason_for_referral', 'notes', 'referred_by',
                    'referred_to_email')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_status', 'first_attempt', 'second_attempt', 'third_attempt', 'appointment_date',
                    'patient', 'practice')


admin.site.register(Practice, PracticeAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(TempReferral, TempReferralAdmin)
admin.site.register(Appointment, AppointmentAdmin)
