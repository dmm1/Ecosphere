# ecosphere\apps\business_partner\urls.py
from django.urls import path
from . import views

app_name = 'business_partner'

urlpatterns = [
    path('businesspartner/', views.businesspartner_list, name='businesspartner_list'),
    path('businesspartner/create/', views.businesspartner_create, name='businesspartner_create'),
    path('businesspartner/<int:pk>/', views.businesspartner_detail, name='businesspartner_detail'),
    path('businesspartner/<int:pk>/update/', views.businesspartner_update, name='businesspartner_update'),
    path('businesspartner/<int:pk>/delete/', views.businesspartner_delete, name='businesspartner_delete'),

]