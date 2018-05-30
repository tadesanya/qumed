from django.urls import path
from . import views


app_name = 'referral'


urlpatterns = [
    path('create_practice', views.CreatePracticeView.as_view(), name='create_practice')
]
