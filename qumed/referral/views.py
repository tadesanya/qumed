from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PracticeForm, ReferralForm
from .models import Patient, Practice
from qumed.constants import PAGINATE_30


class CreatePracticeView(LoginRequiredMixin, View):

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


class PatientsListView(LoginRequiredMixin, ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = 'referral/list_patients.html'
    paginate_by = PAGINATE_30

    def get_queryset(self):
        practice = self.request.user.practice
        queryset = Patient.objects.filter(current_practice=practice)
        return queryset


class PatientCreateView(LoginRequiredMixin, CreateView):
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


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'referral/patient_detail.html'


class ReferralCreateView(LoginRequiredMixin, View):
    template_name = 'referral/create_referral.html'

    def get(self, request, **kwargs):
        referral_form = ReferralForm()
        patient = get_object_or_404(Patient, id=kwargs['pk'])
        practices = get_list_or_404(Practice)
        return render(request, self.template_name, {'patient': patient,
                                                    'referral_form': referral_form,
                                                    'practices': practices})

    def post(self, request):
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral = form.save()
            message = "Patient has been referred to {}, you will be notified when they accept the referral".format(
                referral.referred_to.name)
            messages.success(request, message)
            return HttpResponseRedirect(reverse_lazy('account:dashboard'))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse_lazy('referral:create_referral'))
