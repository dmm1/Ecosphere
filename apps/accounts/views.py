from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfilePictureForm, UserProfileUpdateForm
from apps.hr.models import Employee, Department, Position


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
    return render(request, 'apps/accounts/login.html', {'error_message': error_message})

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created or not user_profile.employee:
        default_department, _ = Department.objects.get_or_create(name='Default')
        default_position, _ = Position.objects.get_or_create(title='Default')
        employee, _ = Employee.objects.get_or_create(user=request.user, defaults={'department': default_department, 'position': default_position})
        user_profile.employee = employee
        user_profile.save()

    if request.method == 'POST':
        user_profile.bio = request.POST.get('bio')
        user_profile.profile_picture = request.FILES.get('profile_picture')
        user_profile.country = request.POST.get('country')
        user_profile.language = request.POST.get('language')
        user_profile.timezone = request.POST.get('timezone')
        user_profile.user.first_name = request.POST.get('first_name')
        user_profile.user.last_name = request.POST.get('last_name')
        user_profile.user.email = request.POST.get('email')
        user_profile.user.save()
        print(f"POST phone_number: {request.POST.get('phone_number')}")
        if user_profile.employee:
            user_profile.employee.phone_number = request.POST.get('phone_number')
            user_profile.employee.save()
            print(f"Employee phone_number after save: {user_profile.employee.phone_number}")
        user_profile.save()
        return redirect('accounts:profile')

    print(f"Employee phone_number: {user_profile.employee.phone_number if user_profile.employee else 'No employee'}")
    context = {
        'user_profile': user_profile,
        'phone_number': user_profile.employee.phone_number if user_profile.employee else ''
    }
    return render(request, 'apps/accounts/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if not profile.employee:
        profile.employee, _ = Employee.objects.get_or_create(user=user, defaults={'department_id': user.department_id})  # Set the department_id
        profile.save()

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            profile.bio = form.cleaned_data['bio']
            profile.employee.phone_number = form.cleaned_data['phone_number']
            profile.country = form.cleaned_data['country']
            profile.language = form.cleaned_data['language']
            profile.timezone = form.cleaned_data['timezone']
            profile.employee.save()  # Save the employee object
            profile.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileUpdateForm(instance=profile, user=user)
    context = {
        'form': form,
        'phone_number': profile.employee.phone_number if profile.employee else None
    }
    return render(request, 'apps/accounts/edit_profile.html', context)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
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
    return render(request, 'apps/accounts/change_profile_picture.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')