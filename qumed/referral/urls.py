from django.urls import path

from . import views


app_name = 'referral'


urlpatterns = [
    path('practice/create/', views.CreatePracticeView.as_view(), name='create_practice'),
    path('patients/view/', views.PatientsListView.as_view(), name='view_patients'),
    path('patient/create/', views.PatientCreateView.as_view(), name='create_patient'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),

    path('create/<int:pk>/', views.ReferralCreateView.as_view(), name='create_referral')
]
