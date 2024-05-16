from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Country, Group, Team, CountryAdmin, User, CountrySetting
from .serializers import UserSerializer, GroupSerializer, TeamSerializer, CountrySerializer, CountrySettingSerializer
from .forms import UserForm, GroupForm, TeamForm, UserUpdateForm, GroupUpdateForm, TeamUpdateForm, UserCreationForm, CountrySettingForm
from .models import CountrySetting
from .serializers import CountrySettingSerializer
from django.contrib import messages
import logging
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

class UserAutocompleteView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        users = User.objects.filter(username__icontains=query)
        data = []
        for user in users:
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'country': user.country if hasattr(user, 'country') else 'Not available',
            }
            data.append(user_data)
        return Response(data, status=status.HTTP_200_OK)

def user_autocomplete(request):
    term = request.GET.get('q')
    users = User.objects.filter(
        Q(username__icontains=term) |
        Q(first_name__icontains=term) |
        Q(last_name__icontains=term)
    )
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'text': f"{user.first_name} {user.last_name} - {user.email} ({user.country or  _('Not available')})"
        })
    return JsonResponse({'results': data})

@login_required
def dashboard(request):
    users = User.objects.filter(countryadmin__country=request.user.countryadmin.country)
    groups = Group.objects.filter(country=request.user.countryadmin.country)
    teams = Team.objects.filter(group__country=request.user.countryadmin.country)
    visits = request.session.get('visits', 0)
    country_setting = CountrySetting.objects.all()
    request.session['visits'] = visits + 1
    return render(request, 'apps/organization/dashboard.html', {'visits': visits, 'users': users, 'groups': groups, 'teams': teams, 'country_setting': country_setting})

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
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'apps/organization/group_detail.html', {'group': group})

@login_required
def create_group(request):
    if request.user.has_perm('organization.add_group'):
        if request.method == 'POST':
            form = GroupForm(request.user, request.POST)
            if form.is_valid():
                group = form.save()
                group.permissions.set(form.cleaned_data['permissions'])
                messages.success(request, 'Group created successfully.')
                return redirect('organization:dashboard')
        else:
            form = GroupForm(request.user)
        return render(request, 'apps/organization/create_group.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to create a group.')
        return redirect('organization:dashboard')

@login_required
def group_list(request):
    groups = Group.objects.filter(country=request.user.countryadmin.country)
    return render(request, 'apps/organization/group_list.html', {'groups': groups})


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
            group = form.save()
            group.permissions.set(form.cleaned_data['permissions'])
            messages.success(request, 'Group updated successfully.')
            return redirect('organization:group_list')
    else:
        form = GroupUpdateForm(instance=group)
    return render(request, 'apps/organization/update_group.html', {'form': form})


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully.')
        return redirect('organization:group_list')
    return render(request, 'apps/organization/confirm_delete.html', {'object': group})

@login_required
def team_list(request):
    teams = Team.objects.filter(group__country=request.user.countryadmin.country)
    return render(request, 'apps/organization/team_list.html', {'teams': teams})

@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team_members_list = list(team.members.all().values('id', 'username', 'first_name', 'last_name', 'email', 'countryadmin__country__name'))
    return render(request, 'apps/organization/team_detail.html', {'team': team, 'team_members_list': team_members_list})

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, user=request.user)
        if form.is_valid():
            team = form.save()
            return redirect('organization:team_detail', team_id=team.id)
    else:
        form = TeamForm(user=request.user)
    return render(request, 'apps/organization/create_team.html', {'form': form})


@login_required
def read_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'apps/organization/team_detail.html', {'team': team})


@login_required
def team_update(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamUpdateForm(request.POST, instance=team, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('organization:team_detail', team.id)
    else:
        form = TeamUpdateForm(instance=team, user=request.user)

    all_users = User.objects.all()
    team_members_list = list(team.members.all().values('id', 'username', 'first_name', 'last_name', 'email', 'countryadmin__country__name'))

    context = {
        'team': team,
        'form': form,
        'all_users': all_users,
        'team_members_list': team_members_list,
    }
    return render(request, 'apps/organization/update_team.html', context)


@login_required
def team_delete(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        team.delete()
        return redirect('organization:team_list')
    return render(request, 'apps/organization/team_confirm_delete.html', {'team': team})


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminUser]  # Only allow superusers

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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


class CountrySettingViewSet(viewsets.ModelViewSet):
    queryset = CountrySetting.objects.all()
    serializer_class = CountrySettingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CountrySetting.objects.all()
        elif hasattr(self.request.user, 'countryadmin'):
            return CountrySetting.objects.filter(country=self.request.user.countryadmin.country)
        else:
            return CountrySetting.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser and self.request.user.countryadmin.country != serializer.validated_data['country']:
            raise permissions.PermissionDenied("You can't create a country setting for this country.")
        serializer.save()

@login_required
def country_setting_create(request):
    if request.method == 'POST':
        form = CountrySettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # replace with the name of the view you want to redirect to
    else:
        form = CountrySettingForm()
    return render(request, 'apps/organization/create_countrysetting.html', {'form': form})

@login_required
def country_setting_list(request):
    country_setting = CountrySetting.objects.all()
    return render(request, 'apps/organization/country_setting_list.html', {'country_setting': country_setting})

@login_required
def country_setting_detail(request, country_setting_id):
    country_setting = get_object_or_404(CountrySetting, id=country_setting_id)
    return render(request, 'apps/organization/country_setting_detail.html', {'country_setting': country_setting})

@login_required
def country_setting_update(request, country_setting_id):
    country_setting = get_object_or_404(CountrySetting, id=country_setting_id)
    if request.method == 'POST':
        form = CountrySettingForm(request.POST, instance=country_setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Country Setting updated successfully.')
            return redirect('organization:country_setting_list')
    else:
        form = CountrySettingForm(instance=country_setting)
    return render(request, 'apps/organization/update_country_setting.html', {'form': form})

@login_required
def country_setting_delete(request, country_setting_id):
    country_setting = get_object_or_404(CountrySetting, id=country_setting_id)
    if request.method == 'POST':
        country_setting.delete()
        messages.success(request, 'Country Setting deleted successfully.')
        return redirect('organization:country_setting_list')
    return render(request, 'apps/organization/confirm_delete.html', {'object': country_setting})