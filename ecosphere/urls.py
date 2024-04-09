from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view
from .models import Customer

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # This line includes Django's set_language view
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', views.admin_view, name='admin'),
    path('user/dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customers'),
    path('customers_index', views.customers_index, name='customers_index'),
]
