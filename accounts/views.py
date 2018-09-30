from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, authenticate, login as django_login
from django.contrib.auth.models import User
from .models import Info

# Create your views here.

def settings(request, username):
    if not request.user.is_authenticated:
        return redirect('library:index')
    else:
        user = User.objects.get(username=username)
        if request.user == user:
            return render(request, 'accounts/settings.html')

    return redirect('library:index')

def logout(request):
    django_logout(request)
    return redirect('library:index')

def login_view(request):
    if request.user.is_authenticated:
        try:
            request.user.info
        except:
            new_user_info = Info.objects.create(user=request.user)
            return render(request, 'accounts/settings.html', {'first_time': True})
            #return redirect('accounts:settings', username=request.user.username)

    print('testuojam')
    print(request.path)
    return redirect('library:index')

def login_old_view(request):
    if request.method == "POST":
        username = request.POST.get("login_username")
        password = request.POST.get("login_password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)

    return redirect('library:index')

