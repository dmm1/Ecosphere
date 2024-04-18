# ecosphere\crm\urls.py
from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('businesspartner/', views.businesspartner_list, name='businesspartner_list'),
    path('businesspartner/create/', views.businesspartner_create, name='businesspartner_create'),
    path('businesspartner/<int:pk>/', views.businesspartner_detail, name='businesspartner_detail'),
    path('businesspartner/<int:pk>/update/', views.businesspartner_update, name='businesspartner_update'),
    path('businesspartner/<int:pk>/delete/', views.businesspartner_delete, name='businesspartner_delete'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/create/', views.opportunity_create, name='opportunity_create'),
    path('opportunities/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunities/<int:pk>/update/', views.opportunity_update, name='opportunity_update'),
    path('opportunities/<int:pk>/delete/', views.opportunity_delete, name='opportunity_delete'),
]
