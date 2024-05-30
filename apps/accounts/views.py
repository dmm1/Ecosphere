from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.decorators import login_required
from.models import UserProfile
from.forms import ProfilePictureForm, UserProfileUpdateForm
from apps.company.models import Employee, Department, Position, Company, Team 
from django.http import JsonResponse

def login_view(request):
    error_message = ''  # Define error_message here or generate it dynamically based on some condition

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            refresh = RefreshToken.for_user(user)
            # Store the refresh token in a cookie
            response = redirect('crm:dashboard')
            response.set_cookie('refresh', str(refresh))
            # Store the access token in a cookie
            response.set_cookie('access', str(refresh.access_token))
            return response
        else:
            error_message = 'Invalid Credentials'
            return JsonResponse({'error': error_message}, status=401)

    return render(request, 'apps/accounts/login.html', {'error_message': error_message})

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created or not user_profile.employee:
        default_company, _ = Company.objects.get_or_create(name='Default')  # Create a Company object first
        default_department, _ = Department.objects.get_or_create(name='Default', company=default_company)  # Provide the Company object when creating a Department object
        default_position, _ = Position.objects.get_or_create(title='Default', company=default_company)  # Provide the Company object when creating a Position object
        default_team, _ = Team.objects.get_or_create(title='Default', company=default_company)
        employee, _ = Employee.objects.get_or_create(user=request.user, defaults={'department': default_department, 'position': default_position, 'company': default_company, 'team': default_team})
        user_profile.employee = employee
        user_profile.save()

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')

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
        default_company, _ = Company.objects.get_or_create(name='Default')
        default_department, _ = Department.objects.get_or_create(name='Default', company=default_company)
        default_position, _ = Position.objects.get_or_create(title='Default', company=default_company)
        default_team, _ = Team.objects.get_or_create(title='Default', company=default_company)
        profile.employee, _ = Employee.objects.get_or_create(user=user, defaults={'department': default_department, 'position': default_position, 'company': default_company, 'team': default_team})
        profile.save()

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileUpdateForm(instance=profile, user=user)
    context = {
        'form': form,
        'phone_number': profile.employee.phone_number if profile.employee else None
    }
    return render(request, 'apps/accounts/edit_profile.html', context)

@login_required
def handle_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    return redirect('accounts:profile')

@login_required
def upload_profile_picture(request):
    return handle_profile_picture(request)

@login_required
def change_profile_picture(request):
    if request.method == 'POST':
        return handle_profile_picture(request)
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    return render(request, 'apps/accounts/change_profile_picture.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')