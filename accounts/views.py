from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.forms import RegistrationForm, AccountUpdateForm

from .models import Account


class AccountRegisterView( CreateView ):

    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Account created'


class AccountUpdateView( UpdateView ):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('store')


def profile( request ):
    form_class = AccountUpdateForm
    context = {'user': request.user }
    return render( request, 'accounts/profile.html', context)