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
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/update/', views.contact_update, name='contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/create/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/update/', views.lead_update, name='lead_update'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),
]
