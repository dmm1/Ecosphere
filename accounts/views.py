from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.urls import reverse
from django.shortcuts import redirect

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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('crm:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('ecosphere:index')


# Create your views here.
