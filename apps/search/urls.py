from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('search/', views.search_results, name='search_results'),
]