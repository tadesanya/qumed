from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .forms import PracticeForm, ReferralForm, AcceptRejectForm, TempReferralForm
from .models import Patient, Practice, Referral
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
        user_practice_id = request.user.practice.id
        practices = get_list_or_404(Practice, ~Q(id=user_practice_id))
        return render(request, self.template_name, {'patient': patient,
                                                    'referral_form': referral_form,
                                                    'practices': practices})

    def post(self, request, **kwargs):
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral = form.save()

            # Send referral notification email
            current_site = get_current_site(self.request)
            subject = 'Patient Referral from {}'.format(referral.referred_by.name)
            email_body = render_to_string('referral/referral_notification_email.txt', {'domain': current_site,
                                                                                       'patient': referral.patient})
            recipients = [referral.referred_to.email]
            email = EmailMessage(subject=subject, body=email_body, to=recipients)
            email.send()

            message = "{} has been referred to {}, you will be notified when they accept the referral".format(
                referral.patient.name, referral.referred_to.name)
            messages.success(request, message)

            return HttpResponseRedirect(reverse_lazy('account:dashboard'))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse_lazy('referral:create_referral', kwargs={'pk': request.POST['patient']}))


class ReferByEmailView(LoginRequiredMixin, View):

    def post(self, request):
        form = TempReferralForm(request.POST)
        if form.is_valid():
            temp_referral = form.save()

            # Send email to receiving practice, with encoded TempReferral object id
            practice_name = request.user.practice.name
            current_site = get_current_site(self.request)
            email_subject = 'Patient Referral From {}'.format(practice_name.title())
            email_message = render_to_string('referral/patient_referral_email.txt',
                                             {'domain': current_site.domain,
                                              'encoded_id': force_text(urlsafe_base64_encode(force_bytes(temp_referral.id))),
                                              'temp_referral': temp_referral,
                                              })
            recipients = [temp_referral.referred_to_email]
            email = EmailMessage(subject=email_subject, body=email_message, to=recipients)
            email.send()

            message = 'An email has been sent to the practice, to view details of the referral on our platform.'
            messages.success(request, message)

            return HttpResponseRedirect(reverse_lazy('account:dashboard'))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse_lazy('referral:create_referral', kwargs={'pk': request.POST['patient']}))


class ReferralListView(LoginRequiredMixin, ListView):
    model = Referral
    context_object_name = 'referrals'
    template_name = 'referral/list_referrals.html'
    paginate_by = PAGINATE_30

    def get_queryset(self):
        practice = self.request.user.practice
        viewset = self.kwargs['viewset']
        if viewset == 'outgoing':
            queryset = Referral.objects.filter(referred_by=practice)
        else:
            queryset = Referral.objects.filter(referred_to=practice, referral_status=viewset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewset'] = self.kwargs['viewset']
        return context


class AcceptRejectReferralView(LoginRequiredMixin, View):

    def post(self, request):
        form = AcceptRejectForm(request.POST)
        if form.is_valid():
            referral_id = form.cleaned_data['referral_id']
            referral_status = form.cleaned_data['referral_status']
            if referral_status != 'pending':
                referral = get_object_or_404(Referral, id=referral_id)
                referral.referral_status = referral_status
                referral.save()
                message = 'You have {} the referral.'.format(referral_status)
                messages.info(request, message)

                return HttpResponseRedirect(reverse_lazy('referral:list_referrals', kwargs={'viewset': 'pending'}))
            else:
                message = 'Invalid referral response given'
                messages.error(request, message)
                return HttpResponseRedirect(reverse_lazy('referral:list_referrals', kwargs={'viewset': 'pending'}))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse_lazy('referral:list_referrals', kwargs={'viewset': 'pending'}))


class OnboardingStage1(View):
    pass
