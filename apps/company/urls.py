from django.urls import include, path
from . import views  
from .views import Home, test_auth, get_user_details

app_name = 'employees'

urlpatterns = [
    path('', views.index, name='hr_index'),
    path('api/', Home.as_view()),
    path('test-auth/', test_auth, name='test-auth'),
    path('employee/get_user_details/', get_user_details, name='get_user_details'),
    path('employee/', views.index, name='hr_index'),
    path('employee/create', views.create_employee, name='create_employee'),
    path('employee/list', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/update/', views.edit_employee, name='edit_employee'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('department/', views.department_list, name='department_list'),
    path('department/create', views.create_department, name='create_department'),
    path('department/list', views.department_list, name='department_list'),
    path('department/<int:pk>/edit/', views.edit_department, name='edit_department'),
    path('department/<int:pk>/', views.department_detail, name='department_detail'),
    path('position/', views.position_list, name='position_list'),
    path('position/create', views.create_position, name='create_position'),
    path('position/list', views.position_list, name='position_list'),
    path('position/<int:pk>/edit/', views.edit_position, name='edit_position'),
    path('position/<int:pk>/', views.position_detail, name='position_detail'),
    path('team/', views.team_list, name='team_list'),
    path('team/create', views.create_team, name='create_team'),
    path('team/list', views.team_list, name='team_list'),
    path('team/<int:pk>/edit/', views.edit_team, name='edit_team'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
]
