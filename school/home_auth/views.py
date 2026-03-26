# home_auth/views.py
from django.shortcuts import render, redirect


def signup_view(request):
    return render(request, 'authentication/signup.html')


def login_view(request):
    return render(request, 'authentication/login.html')


def logout_view(request):
    return redirect('login')
