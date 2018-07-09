from django.urls import path

from . import views


app_name = 'referral'


urlpatterns = [
    path('practice/create/', views.CreatePracticeView.as_view(), name='create_practice'),
    path('patients/view/', views.PatientsListView.as_view(), name='view_patients'),
    path('patient/create/', views.PatientCreateView.as_view(), name='create_patient'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),

    path('create/<int:pk>/', views.ReferralCreateView.as_view(), name='create_referral'),
    path('incoming/<str:viewset>/', views.ReferralListView.as_view(), name='list_referrals'),
    path('decide/', views.AcceptRejectReferralView.as_view(), name='decide_on_referral'),
    path('email/', views.ReferByEmailView.as_view(), name='email_referral'),

    path('onboard/1/<temp_referral_id>', views.OnboardingStage1.as_view(), name='onboard_1')
]
