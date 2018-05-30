from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView

from .forms import PracticeForm
from .models import Patient
from qumed.constants import PAGINATE_30


class CreatePracticeView(View):

    def post(self, request):
        form = PracticeForm(request.POST)
        if form.is_valid():
            practice = form.save(commit=False)
            practice.created_by = request.user
            practice.save()
            request.user.practice = practice
            request.user.save()

            message = 'You have successfully created and have been added to the practice: {}'.format(practice.name)
            messages.success(request, message)
            return HttpResponseRedirect(reverse_lazy('account:dashboard'))
        else:
            message = form.errors
            messages.error(request, message)
            return HttpResponseRedirect(reverse_lazy('account:link_practice'))


class ListPatientsView(ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = 'referral/list_patients.html'
    paginate_by = PAGINATE_30

    def get_queryset(self):
        practice = self.request.user.practice
        queryset = Patient.objects.filter(current_practice=practice)
        return queryset


class CreatePatientView(CreateView):
    model = Patient
    fields = ['mrn', 'name', 'address', 'email', 'telephone']
    template_name = 'referral/create_patient.html'
    success_url = reverse_lazy('referral:view_patients')

    def form_valid(self, form):
        # Set creator and current practice on the patient object created
        practice = self.request.user.practice
        self.object = form.save(commit=False)
        self.object.creator_practice = practice
        self.object.current_practice = practice
        self.object.save()

        message = 'New patient created.'
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())
