from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as django_logout, authenticate, login as django_login
from django.contrib.auth.models import User
from .models import Info

# Create your views here.


def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user_profile': user
    }
    return render(request, 'accounts/profile.html', context)

def settings(request, username):
    if not request.user.is_authenticated:
        return redirect('library:index')
    else:
        user = get_object_or_404(User, username=username)
        # user = User.objects.get(username=username)
        if request.user == user:
            request.method == "POST"
            avatar = None if not request.FILES.get('avatar') else request.FILES.get('avatar')
            birth_date = request.POST.get('birth_date')
            phone_num = request.POST.get('phone_number')
            info = Info.objects.get(user=request.user)
            if request.FILES.get('avatar'):
                info.avatar = avatar
            if request.POST.get('birth_date'):
                info.phone_number = phone_num
            if request.POST.get('phone_number'):
                info.birth_date = birth_date
            info.save()

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
