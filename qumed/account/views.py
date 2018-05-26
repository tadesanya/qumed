from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages

from .forms import CustomUserCreationForm
from .tokens import account_activation_token


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account:registration_complete')
    template_name = 'signup.html'

    def form_valid(self, form):
        # send activation email
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('registration/activation_email.txt',
                                   {'user': self.object,
                                    'domain': current_site.domain,
                                    'uid': force_text(urlsafe_base64_encode(force_bytes(self.object.pk))),
                                    'token': account_activation_token.make_token(self.object),
                                    })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject,
                             message,
                             to=[to_email])
        email.send()
        return HttpResponseRedirect(self.get_success_url())


class ActivateAccount(View):
    def get(self, request, *args, **kwargs):
        User = get_user_model()

        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)
            message = 'Account activation successful.'
            messages.success(request, message)
            return HttpResponseRedirect(reverse_lazy('account:dashboard'))
        else:
            message = 'Activation link is invalid!'
            messages.error(request, message)
            return HttpResponseRedirect(reverse_lazy('account:activation_fail'))


class Dashboard(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
