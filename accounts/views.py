from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.forms import RegistrationForm


class AccountRegisterView( generic.CreateView ):

    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Account created'

     

def register( request ):
    context = {}
    return HttpResponse('Register')

def signin( request ):
    context = {}
    return render( request, 'accounts/signin.html', context )

def signup( request ):
    context = {}
    return render( request, 'accounts/signup.html', context )

