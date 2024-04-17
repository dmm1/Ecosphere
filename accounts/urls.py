# ecosphere\accounts\urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import login_view, logout_view, profile_view, upload_profile_picture, change_profile_picture

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('profile/change_profile_picture/', login_required(change_profile_picture), name='change_profile_picture'),
]