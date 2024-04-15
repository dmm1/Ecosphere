from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer, Opportunity
from .forms import OpportunityForm, CustomerForm


def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def customer_list(request):
    customers = request.user.customers.all()
    return render(request, 'crm/customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'crm/customer_detail.html', {'customer': customer})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect('crm:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'crm/customer_form.html', {'form': form})
@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('crm:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_form.html', {'form': form, 'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('crm:customer_list')
    return render(request, 'crm/customer_confirm_delete.html', {'customer': customer})

@login_required
def opportunity_list(request):
    opportunities = request.user.opportunities.all()
    return render(request, 'crm/opportunity_list.html', {'opportunities': opportunities})

@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, assigned_to=request.user)
    return render(request, 'crm/opportunity_detail.html', {'opportunity': opportunity})

@login_required
def opportunity_create(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.assigned_to = request.user
            opportunity.save()
            return redirect('crm:opportunity_list')
    else:
        form = OpportunityForm()
    return render(request, 'crm/opportunity_form.html', {'form': form})
@login_required
def opportunity_update(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect('crm:opportunity_list')
    else:
        form = OpportunityForm(instance=opportunity)
    return render(request, 'crm/opportunity_form.html', {'form': form, 'opportunity': opportunity})

@login_required
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        opportunity.delete()
        return redirect('crm:opportunity_list')
    return render(request, 'crm/opportunity_confirm_delete.html', {'opportunity': opportunity})