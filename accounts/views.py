# ecosphere\accounts\views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.urls import reverse
from django.shortcuts import redirect

def index(request):
    return render(request, 'ecosphere/index.html')
@login_required
def profile_view(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_profile.bio = request.POST.get('bio')
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.profile_picture = request.FILES.get('profile_picture')
        user_profile.save()
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'user_profile': user_profile})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Use the imported authenticate function
        if user is not None:
            login(request, user)
            return redirect('crm:dashboard')
        else:
            error_message = 'Invalid username or password'
    return render(request, 'ecosphere/index.html', {'error_message': error_message})
def logout_view(request):
    logout(request)
    return redirect('ecosphere:index')


# Create your views here.
