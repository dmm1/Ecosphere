from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm, DepartmentForm, PositionForm
from .models import Employee, Department, Position
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    employee_list = Employee.objects.all().order_by('id')
    department_list = Department.objects.all().order_by('id')
    position_list = Position.objects.all().order_by('id')

    paginator = Paginator(employee_list, 10) # Show 10 employees per page
    page_number = request.GET.get('employee_page')
    page_obj_employee = paginator.get_page(page_number)

    paginator = Paginator(department_list, 10) # Show 10 departments per page
    page_number = request.GET.get('department_page')
    page_obj_department = paginator.get_page(page_number)

    paginator = Paginator(position_list, 10) # Show 10 positions per page
    page_number = request.GET.get('position_page')
    page_obj_position = paginator.get_page(page_number)

    context = {
        'page_obj_employee': page_obj_employee,
        'page_obj_department': page_obj_department,
        'page_obj_position': page_obj_position,
    }

    return render(request, 'apps/company/dashboard.html', context)

def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'apps/company/create_employee.html', {'form': form})

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_detail', pk=employee.pk)  
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'apps/company/edit_employee.html', {'form': form})

def employee_list(request):
    search_query = request.GET.get('search', '')
    employees = Employee.objects.filter(
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query) |
        Q(user__email__icontains=search_query)
    )
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj_employee = paginator.get_page(page_number)  # Changed from page_obj to page_obj_employee
    return render(request, 'apps/company/employee_list.html', {'page_obj_employee': page_obj_employee})  # Changed from page_obj to page_obj_employee


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'apps/company/employee_detail.html', {'employee': employee})

def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'apps/company/create_department.html', {'form': form})

def create_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:position_list')
    else:
        form = PositionForm()
    return render(request, 'apps/company/create_position.html', {'form': form})

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


def department_list(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.filter(
        Q(name__icontains=search_query)
    )
    paginator = Paginator(departments, 10)  # Show 10 departments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'apps/company/department_list.html', {'page_obj': page_obj})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'apps/company/department_detail.html', {'department': department})

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

def position_list(request):
    search_query = request.GET.get('search', '')
    positions = Position.objects.filter(
        Q(title__icontains=search_query)
    )
    paginator = Paginator(positions, 10)  # Show 10 positions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'apps/company/position_list.html', {'page_obj': page_obj})

def position_detail(request, pk):
    position = get_object_or_404(Position, pk=pk)
    return render(request, 'apps/company/position_detail.html', {'position': position})
