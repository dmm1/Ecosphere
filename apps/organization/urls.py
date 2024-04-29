# apps/organization/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, TeamViewSet, CountryViewSet, dashboard, create_user, read_user, update_user, delete_user, create_group, read_group, update_group, delete_group, create_team, read_team, update_team, delete_team, user_profile
from . import views

app_name = 'organization'

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'teams', TeamViewSet, basename='team')

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/user/', create_user, name='create_user.html'),
    path('read/user/<int:user_id>/', read_user, name='read_user'),
    path('update/user/<int:user_id>/', update_user, name='update_user'),
    path('delete/user/<int:user_id>/', delete_user, name='delete_user'),
    path('create/group/', create_group, name='create_group'),
    path('read/group/<int:group_id>/', read_group, name='read_group'),
    path('update/group/<int:group_id>/', update_group, name='update_group'),
    path('delete/group/<int:group_id>/', delete_group, name='delete_group'),
    path('create/team/', create_team, name='create_team'),
    path('read/team/<int:team_id>/', read_team, name='read_team'),
    path('update/team/<int:team_id>/', update_team, name='update_team'),
    path('delete/team/<int:team_id>/', delete_team, name='delete_team'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
]


urlpatterns += router.urls