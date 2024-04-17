from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect the user to the appropriate page after login
            return redirect('crm:dashboard')  # or any other URL you want to redirect to
        else:
            error_message = 'Invalid username or password'
    return render(request, 'accounts/login.html', {'error_message': error_message})

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

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('accounts:profile')
    else:
        return redirect('accounts:profile')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
