from django.urls import path

from . import views


app_name = 'referral'


urlpatterns = [
    path('create_practice', views.CreatePracticeView.as_view(), name='create_practice'),
    path('view_patients', views.ListPatientsView.as_view(), name='view_patients'),
    path('create_patient', views.CreatePatientView.as_view(), name='create_patient'),
]
