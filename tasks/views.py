# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    show_all = str(request.session.get('show_all', False)).lower()
    if 'show_all' in request.GET:
        show_all = str(request.GET.get('show_all', 'false')).lower() == 'true'
        request.session['show_all'] = show_all

    if show_all:
        tasks = Task.objects.all().order_by('due_date')
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')

    paginator = Paginator(tasks, 5)  # Show 5 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/task_list.html', {'page_obj': page_obj, 'show_all': show_all})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})