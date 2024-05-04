# apps/organization/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, TeamViewSet, CountryViewSet, dashboard, create_user, read_user, update_user, delete_user, create_group, read_group, update_group, delete_group, group_list, group_detail, team_list, team_detail, team_create, team_update, team_delete, user_profile, UserAutocompleteView
from .views import user_autocomplete

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
    path('users/autocomplete/', UserAutocompleteView.as_view(), name='user_autocomplete'),
    path('groups/<int:group_id>/', read_group, name='read_group'),
    path('groups/', group_list, name='group_list'),
    path('groups/create/', create_group, name='group_create'),
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('groups/<int:group_id>/update/', update_group, name='group_update'),
    path('groups/<int:group_id>/delete/', delete_group, name='group_delete'),
    path('teams/', team_list, name='team_list'),
    path('teams/<int:team_id>/', team_detail, name='team_detail'),
    path('teams/create/', team_create, name='team_create'),
    path('teams/<int:team_id>/update/', team_update, name='team_update'),
    path('teams/<int:team_id>/delete/', team_delete, name='team_delete'),
    path('users/<int:user_id>/profile/', user_profile, name='user_profile'),
    path('api/', include(router.urls)),
    path('user-autocomplete/', user_autocomplete, name='user-autocomplete'),
    path('api/groups/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve'}), name='group-detail'),
]

urlpatterns += router.urls
