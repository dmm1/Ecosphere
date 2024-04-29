from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Country, Group, Team, CountryAdmin
from .serializers import UserSerializer, GroupSerializer, TeamSerializer, CountrySerializer
from .forms import UserForm, GroupForm, TeamForm, UserUpdateForm, GroupUpdateForm, TeamUpdateForm, UserCreationForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    users = User.objects.filter(countryadmin__country=request.user.countryadmin.country)
    groups = Group.objects.filter(country=request.user.countryadmin.country)
    teams = Team.objects.filter(group__country=request.user.countryadmin.country)
    return render(request, 'apps/organization/dashboard.html', {'users': users, 'groups': groups, 'teams': teams})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'apps/organization/user_profile.html', {'user': user})

# Update the create_user view
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.user, data=request.POST)
        if form.is_valid():
            try:
                user = form.save()
                logger.info(f"User '{user.username}' created successfully.")
                return redirect('organization:dashboard')
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                logger.exception(e)  # This will log the exception
    else:
        form = UserCreationForm(request.user)

    logger.debug(f"Rendering create_user.html with form: {form}")
    return render(request, 'apps/organization/create_user.html', {'form': form})

@login_required
def read_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'apps/organization/user_detail.html', {'user': user})

@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('organization:dashboard')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'apps/organization/update_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('organization:dashboard')
    return render(request, 'apps/organization/confirm_delete.html', {'object': user})

@login_required
def create_group(request):
    if request.user.has_perm('organization.add_group'):
        if request.method == 'POST':
            form = GroupForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Group created successfully.')
                return redirect('organization:dashboard')
        else:
            form = GroupForm(request.user)
        return render(request, 'apps/organization/create_group.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to create a group.')
        return redirect('organization:dashboard')

@login_required
def read_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'apps/organization/group_detail.html', {'group': group})

@login_required
def update_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupUpdateForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group updated successfully.')
            return redirect('organization:dashboard')
    else:
        form = GroupUpdateForm(instance=group)
    return render(request, 'apps/organization/update_group.html', {'form': form})


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully.')
        return redirect('organization:dashboard')
    return render(request, 'apps/organization/confirm_delete.html', {'object': group})

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            messages.success(request, 'Team created successfully.')
            return redirect('organization:dashboard')
    else:
        form = TeamForm()
    return render(request, 'apps/organization/create_team.html', {'form': form})

@login_required
def read_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'apps/organization/team_detail.html', {'team': team})

@login_required
def update_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamUpdateForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully.')
            return redirect('organization:dashboard')
    else:
        form = TeamUpdateForm(instance=team)
    return render(request, 'apps/organization/update_team.html', {'form': form})

@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Team deleted successfully.')
        return redirect('organization:dashboard')
    return render(request, 'apps/organization/confirm_delete.html', {'object': team})
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminUser]  # Only allow superusers

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Group.objects.all()
        elif hasattr(self.request.user, 'countryadmin'):
            return Group.objects.filter(country=self.request.user.countryadmin.country)
        else:
            return Group.objects.none()

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Team.objects.all()
        elif hasattr(self.request.user, 'countryadmin'):
            return Team.objects.filter(group__country=self.request.user.countryadmin.country)
        else:
            return Team.objects.none()

    def perform_create(self, serializer):
        group = serializer.validated_data['group']
        if group.country != self.request.user.countryadmin.country:
            raise permissions.PermissionDenied("You can't create a team in this group.")
        serializer.save(created_by=self.request.user)

# Update the UserViewSet
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif hasattr(self.request.user, 'countryadmin'):
            return User.objects.filter(countryadmin__country=self.request.user.countryadmin.country)
        else:
            return User.objects.none()


