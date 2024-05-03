# apps/organization/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, TeamViewSet, CountryViewSet, dashboard, create_user, read_user, update_user, delete_user, create_group, read_group, update_group, delete_group, team_list, team_detail, team_create, team_update, team_delete, user_profile, user_autocomplete

app_name = 'organization'

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'teams', TeamViewSet, basename='team')

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:user_id>/', read_user, name='read_user'),
    path('users/<int:user_id>/update/', update_user, name='update_user'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('users/autocomplete/', user_autocomplete, name='user_autocomplete'),
    path('groups/create/', create_group, name='create_group'),
    path('groups/<int:group_id>/', read_group, name='read_group'),
    path('groups/<int:group_id>/update/', update_group, name='update_group'),
    path('groups/<int:group_id>/delete/', delete_group, name='delete_group'),
    path('teams/', team_list, name='team_list'),
    path('teams/<int:team_id>/', team_detail, name='team_detail'),
    path('teams/create/', team_create, name='team_create'),
    path('teams/<int:team_id>/update/', team_update, name='team_update'),
    path('teams/<int:team_id>/delete/', team_delete, name='team_delete'),
    path('users/<int:user_id>/profile/', user_profile, name='user_profile'),
]

urlpatterns += router.urls
