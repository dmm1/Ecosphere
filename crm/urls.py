from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/create/', views.opportunity_create, name='opportunity_create'),
    path('opportunities/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunities/<int:pk>/update/', views.opportunity_update, name='opportunity_update'),
    path('opportunities/<int:pk>/delete/', views.opportunity_delete, name='opportunity_delete'),
]
