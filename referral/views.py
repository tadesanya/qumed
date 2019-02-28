from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.utils import timezone

from .forms import PracticeForm, ReferralForm, AcceptRejectForm, TempReferralForm, AppointmentCreateForm, \
    AppointmentForm
from .models import Patient, Practice, Referral, TempReferral, Appointment
from qumed.constants import PAGINATE_30, REFERRAL_STATUS, APPOINTMENT_FILTER
from account.forms import CustomUserCreationForm


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
        queryset = Patient.objects.filter(Q(current_practice=practice) | Q(creator_practice=practice))
        return queryset


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    fields = ['mrn', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'telephone']
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

    def get_context_data(self, **kwargs):
        context = {}
        patient = self.object
        practice = self.request.user.practice
        appointments = Appointment.objects.filter(practice=practice, patient=patient)
        context['appointments'] = appointments
        context['appointment_form'] = AppointmentCreateForm(initial={'practice': practice.id, 'patient': patient.id})
        kwargs.update(context)
        return super().get_context_data(**kwargs)


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
            if referral_status != REFERRAL_STATUS[0][0]:
                referral = get_object_or_404(Referral, id=referral_id)
                referral.referral_status = referral_status

                if referral_status == REFERRAL_STATUS[1][0]:
                    patient = Patient.objects.get(id=referral.patient.id)
                    patient.current_practice = referral.referred_to
                    patient.save()

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


class OnboardingStage1(CreateView):
    template_name = 'referral/onboard_1.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('referral:onboard_2')

    def get(self, request, *args, **kwargs):
        # Decode the temp_referral_id in the url to check if it exists and add to session
        temp_referral_id = force_text(urlsafe_base64_decode(kwargs['temp_referral_id']))
        get_object_or_404(TempReferral, id=temp_referral_id)
        request.session['temp_referral_id'] = temp_referral_id

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        # Get temp_referral_id from session, to set it in logged in session
        temp_referral_id = self.request.session['temp_referral_id']

        login(self.request, self.object)
        self.request.session['temp_referral_id'] = temp_referral_id
        return HttpResponseRedirect(self.get_success_url())


class OnboardingStage2(LoginRequiredMixin, CreateView):
    template_name = 'referral/onboard_2.html'
    form_class = PracticeForm
    success_url = reverse_lazy('referral:onboard_3')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()

        # Link practice to the user
        self.request.user.practice = self.object
        self.request.user.save()

        # Add the referral to the practise
        temp_referral_id = None
        temp_referral = None

        try:
            temp_referral_id = self.request.session['temp_referral_id']
        except(TypeError, ValueError, KeyError):
            message = 'Error: temp_referral_id does not exist in session.'
            messages.error(self.request, message)
            return HttpResponseRedirect(reverse_lazy('referral:onboard_error'))

        try:
            temp_referral = TempReferral.objects.get(pk=temp_referral_id)
        except TempReferral.DoesNotExist:
            message = 'Error: temp_referral object with that id does not exist.'
            messages.error(self.request, message)
            return HttpResponseRedirect(reverse_lazy('referral:onboard_error'))

        Referral.objects.create(patient=temp_referral.patient,
                                notes=temp_referral.notes,
                                date_referred=temp_referral.date_referred,
                                reason_for_referral=temp_referral.reason_for_referral,
                                referred_by=temp_referral.referred_by,
                                referred_to=self.object)
        temp_referral.delete()

        return HttpResponseRedirect(self.get_success_url())


class AppointmentCreateView(LoginRequiredMixin, View):

    def post(self, request):
        form = AppointmentCreateForm(request.POST)
        referer_url = self.request.META.get('HTTP_REFERER')

        if form.is_valid():
            data = form.cleaned_data
            data['patient'] = get_object_or_404(Patient, id=data['patient'])
            data['practice'] = get_object_or_404(Practice, id=data['practice'])
            appointment = Appointment.objects.create(**data)
            message = 'Appointment created.'
            messages.success(request, message)

            return HttpResponseRedirect(referer_url)
        else:
            message = form.errors
            messages.error(request, message)
            return HttpResponseRedirect(referer_url)


class AppointmentEditView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'referral/appointment_update_form.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        kwargs['patient'] = self.object.patient
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        message = 'Appointment updated.'
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_success_url(self):
        url = self.request.META.get('HTTP_REFERER')
        return url


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    paginate_by = PAGINATE_30
    context_object_name = 'appointments'
    template_name = 'referral/appointment_list.html'

    def get_queryset(self):
        practice = self.request.user.practice
        date_filter = self.kwargs.get('filter', '')
        if date_filter == APPOINTMENT_FILTER['week']:
            this_week = timezone.now().isocalendar()[1]
            queryset = Appointment.objects.filter(practice=practice,
                                                  appointment_date__isnull=False,
                                                  appointment_date__week=this_week)
        elif date_filter == APPOINTMENT_FILTER['month']:
            this_month = timezone.now().month
            queryset = Appointment.objects.filter(practice=practice,
                                                  appointment_date__isnull=False,
                                                  appointment_date__month=this_month)
        elif date_filter == APPOINTMENT_FILTER['today']:
            today = timezone.now().date()
            queryset = Appointment.objects.filter(practice=practice,
                                                  appointment_date__isnull=False,
                                                  appointment_date__date=today)
        elif date_filter == APPOINTMENT_FILTER['upcoming']:
            today = timezone.now().date()
            queryset = Appointment.objects.filter(practice=practice,
                                                  appointment_date__isnull=False,
                                                  appointment_date__date__gte=today)
        else:
            queryset = Appointment.objects.filter(practice=practice,
                                                  appointment_date__isnull=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = self.kwargs.get('filter', '')
        return context


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'referral/appointment_confirm_delete.html'
    success_url = reverse_lazy('referral:list_appointments', kwargs={'filter': 'all'})

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object, create success message and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        message = 'Appointment deleted.'
        messages.success(self.request, message)
        return HttpResponseRedirect(success_url)
