# /apps/company/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm, DepartmentForm, PositionForm, TeamForm
from .models import Employee, Department, Position, Team
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET

def test_auth(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header:
        return JsonResponse({'message': 'Authorization header received'}, status=200)
    else:
        return JsonResponse({'message': 'Authorization header NOT received.'}, status=403)
    
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
@login_required
def index(request):
    """
    Renders the dashboard page with paginated lists of employees, departments, positions, and teams.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template with the paginated lists of employees, departments, positions, and teams.
    """
    employee_list = Employee.objects.all().order_by('id')
    department_list = Department.objects.all().order_by('id')
    position_list = Position.objects.all().order_by('id')
    team_list = Team.objects.all().order_by('id')  # Add this line

    paginator = Paginator(employee_list, 10)  # Show 10 employees per page
    page_number = request.GET.get('employee_page')
    page_obj_employee = paginator.get_page(page_number)

    paginator = Paginator(department_list, 10)  # Show 10 departments per page
    page_number = request.GET.get('department_page')
    page_obj_department = paginator.get_page(page_number)

    paginator = Paginator(position_list, 10)  # Show 10 positions per page
    page_number = request.GET.get('position_page')
    page_obj_position = paginator.get_page(page_number)

    paginator = Paginator(team_list, 10)  # Show 10 teams per page
    page_number = request.GET.get('team_page')  # Add this line
    page_obj_team = paginator.get_page(page_number)  # Add this line

    context = {
        'page_obj_employee': page_obj_employee,
        'page_obj_department': page_obj_department,
        'page_obj_position': page_obj_position,
        'page_obj_team': page_obj_team,  # Add this line
    }

    return render(request, 'apps/company/dashboard.html', context)
@login_required
def create_employee(request):
        """
        Create a new employee.

        This function handles the creation of a new employee. It expects a POST request
        with the employee data in the request body. If the form is valid, the employee
        is saved and the user is redirected to the employee list page. If the request
        method is not POST, a blank form is rendered.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the request method is POST and the form is valid, the function redirects
            the user to the employee list page.
        - If the request method is not POST, the function renders the create employee
            template with a blank form.

        """
        if request.method == 'POST':
                form = EmployeeForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('employees:employee_list')
        else:
                form = EmployeeForm()
        return render(request, 'apps/company/create_employee.html', {'form': form})

@login_required
def edit_employee(request, pk):
    """
    Edit an existing employee.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the employee to be edited.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the employee with the given primary key does not exist.
    """
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_detail', pk=employee.pk)  
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'apps/company/edit_employee.html', {'form': form})

@login_required
def employee_list(request):
    """
    View function to display a list of employees.

    This function retrieves a search query from the request's GET parameters,
    filters the employees based on the search query, and paginates the results.
    The paginated results are then passed to the 'employee_list.html' template
    for rendering.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object containing the rendered template.

    """
    search_query = request.GET.get('search', '')
    employees = Employee.objects.filter(
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query) |
        Q(user__email__icontains=search_query)
    ).order_by('id')
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj_employee = paginator.get_page(page_number)  
    return render(request, 'apps/company/employee_list.html', {'page_obj_employee': page_obj_employee})

@login_required
def employee_detail(request, pk):
    """
    View function to display the details of an employee.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the employee.

    Returns:
        HttpResponse: The HTTP response object containing the rendered employee detail template.
    """
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'apps/company/employee_detail.html', {'employee': employee})

@login_required
@require_GET
def get_user_details(request):
    user_id = request.GET.get('user')
    if user_id is not None:
        try:
            user = User.objects.get(pk=user_id)
            return JsonResponse({
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        except User.DoesNotExist:
            pass
    return JsonResponse({}, status=404)

@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'apps/company/create_department.html', {'form': form})


@login_required
def create_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:position_list')
    else:
        form = PositionForm()
    return render(request, 'apps/company/create_position.html', {'form': form})

@login_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('employees:department_detail', pk=department.pk)  
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'apps/company/edit_department.html', {'form': form})

@login_required
def department_list(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.filter(
        Q(name__icontains=search_query)
    ).order_by('id')
    paginator = Paginator(departments, 10)  # Show 10 departments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'apps/company/department_list.html', {'page_obj': page_obj})

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'apps/company/department_detail.html', {'department': department})

@login_required
def edit_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('employees:position_detail', pk=position.pk)  
    else:
        form = PositionForm(instance=position)
    return render(request, 'apps/company/edit_position.html', {'form': form})

@login_required
def position_list(request):
    search_query = request.GET.get('search', '')
    positions = Position.objects.filter(
        Q(title__icontains=search_query)
    ).order_by('id')  
    paginator = Paginator(positions, 10)  # Show 10 positions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'apps/company/position_list.html', {'page_obj': page_obj})

@login_required
def position_detail(request, pk):
    position = get_object_or_404(Position, pk=pk)
    return render(request, 'apps/company/position_detail.html', {'position': position})

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:team_list')
    else:
        form = TeamForm()
    return render(request, 'apps/company/create_team.html', {'form': form})

@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('employees:team_detail', pk=team.pk)  
    else:
        form = TeamForm(instance=team)
    return render(request, 'apps/company/edit_team.html', {'form': form})

@login_required
def team_list(request):
    search_query = request.GET.get('search', '')
    teams = Team.objects.filter(
        Q(title__icontains=search_query)
    ).order_by('id') 
    paginator = Paginator(teams, 10)  # Show 10 teams per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'apps/company/team_list.html', {'page_obj': page_obj})

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'apps/company/team_detail.html', {'team': team})
