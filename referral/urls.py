from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'referral'


urlpatterns = [
    path('practice/create/', views.CreatePracticeView.as_view(), name='create_practice'),

    path('patients/view/', views.PatientsListView.as_view(), name='view_patients'),
    path('patient/create/', views.PatientCreateView.as_view(), name='create_patient'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patient/<int:pk>/update/', views.PatientUpdateView.as_view(), name='update_patient'),

    path('create/<int:pk>/', views.ReferralCreateView.as_view(), name='create_referral'),
    path('view/<str:viewset>/', views.ReferralListView.as_view(), name='list_referrals'),
    path('decide/', views.AcceptRejectReferralView.as_view(), name='decide_on_referral'),
    path('email/', views.ReferByEmailView.as_view(), name='email_referral'),

    path('onboard/1/<temp_referral_id>/', views.OnboardingStage1.as_view(), name='onboard_1'),
    path('onboard/2/', views.OnboardingStage2.as_view(), name='onboard_2'),
    path('onboard/3/',
         TemplateView.as_view(template_name='referral/onboard_3.html'),
         name='onboard_3'),
    path('onboard/error/',
         TemplateView.as_view(template_name='referral/onboard_error.html'),
         name='onboard_error'),

    path('appointment/create/', views.AppointmentCreateView.as_view(), name='create_appointment'),
    path('appointment/update/<int:pk>/', views.AppointmentEditView.as_view(), name='update_appointment'),
    path('appointments/view/<str:filter>/', views.AppointmentListView.as_view(), name='list_appointments'),
    path('appointment/delete/<int:pk>/', views.AppointmentDeleteView.as_view(), name='delete_appointment')
]
