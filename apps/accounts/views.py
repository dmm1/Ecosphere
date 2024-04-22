from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfilePictureForm, ProfileForm, UserProfileForm


def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('crm:dashboard')
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
        user_profile.user.first_name = request.POST.get('first_name')
        user_profile.user.last_name = request.POST.get('last_name')
        user_profile.user.email = request.POST.get('email')
        user_profile.user.save()
        user_profile.save()
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'user_profile': user_profile})

@login_required
def edit_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    user_form = UserProfileForm(request.POST or None, instance=user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('accounts:profile')
    else:
        return redirect('accounts:profile')

@login_required
def change_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    return render(request, 'accounts/change_profile_picture.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')