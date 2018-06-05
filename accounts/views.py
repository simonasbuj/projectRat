from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout

# Create your views here.

def logout(request):
    django_logout(request)
    return redirect('/knygos')

def login_view(request):
    print('testuojam')
    return redirect('/knygos')

