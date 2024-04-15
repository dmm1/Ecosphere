from django.urls import path
from . import views

app_name = 'ecosphere'

urlpatterns = [
    path('', views.index, name='index'),
]
