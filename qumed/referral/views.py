from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import PracticeForm


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
            messages.error(request, form)
            return HttpResponseRedirect(reverse_lazy('account:link_practice'))
