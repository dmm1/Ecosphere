from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm
from .models import Employee
from django.db.models import Q

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_detail', pk=employee.pk)  
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'apps/hr/edit_employee.html', {'form': form})

def employee_list(request):
    search_query = request.GET.get('search', '')
    employees = Employee.objects.filter(
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query) |
        Q(user__email__icontains=search_query)
    )
    return render(request, 'apps/hr/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'apps/hr/employee_detail.html', {'employee': employee})

