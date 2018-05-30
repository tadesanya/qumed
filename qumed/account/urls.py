"""qumed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate_account'),
    path('activation_complete/',
         TemplateView.as_view(template_name='registration/activation_complete.html'), name='activation_complete'),
    path('activation_fail/',
         TemplateView.as_view(template_name='registration/activate.html'), name='activation_fail'),
    path('registration_complete/',
         TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    path('link_practice/', views.LinkPracticeView.as_view(), name='link_practice')
]
