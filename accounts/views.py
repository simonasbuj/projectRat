from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

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
    try:
        request.user.info
    except:
        return redirect('accounts:settings', username=request.user.username)
    print('testuojam')
    print(request.path)
    return redirect('library:index')

