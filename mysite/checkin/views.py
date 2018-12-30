from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.core import serializers
from django import forms

from .service.authentication import Signup

# Create your views here.

from django.http import HttpResponse


def index(request):
    context = {}
    return render(request, 'home.html', context)

def signup(request):
    signup = Signup()
    if request.method == 'POST':        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            signup.create_user(form)
            signup.login_user(form, request)
            return redirect('home')
    else:
        form = signup.create_form()

    context = {
        "form":form
    }
    return render(request, 'signup.html', context)