from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .models import BusinessPartner, Opportunity
from .forms import OpportunityForm, BusinessParnterForm
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def businesspartner_list(request):
    show_all = str(request.session.get('show_all', False)).lower()
    if 'show_all' in request.GET:
        show_all = str(request.GET.get('show_all', 'false')).lower() == 'true'
        request.session['show_all'] = show_all

    if show_all:
        businesspartner = BusinessPartner.objects.all().order_by('name')  # Order by name
    else:
        businesspartner = BusinessPartner.objects.filter(user=request.user).order_by('name')  # Order by name

    paginator = Paginator(businesspartner, 10)  # Show 10 businesspartner per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'crm/businesspartner_list.html', {'page_obj': page_obj, 'show_all': show_all})

@login_required
def businesspartner_detail(request, pk):
    businesspartner = get_object_or_404(BusinessPartner, pk=pk)
    return render(request, 'crm/businesspartner_detail.html', {'businesspartner': businesspartner})

@login_required
def businesspartner_create(request):
    if request.method == 'POST':
        form = BusinessParnterForm(request.POST)
        if form.is_valid():
            businesspartner = form.save(commit=False)
            businesspartner.user = request.user
            businesspartner.save()
            return redirect('crm:businesspartner_list')
    else:
        form = BusinessParnterForm()
    return render(request, 'crm/businesspartner_form.html', {'form': form})
@login_required
def businesspartner_update(request, pk):
    businesspartner = get_object_or_404(BusinessPartner, pk=pk)
    if request.method == 'POST':
        form = BusinessParnterForm(request.POST, instance=businesspartner)
        if form.is_valid():
            form.save()
            return redirect('crm:businesspartner_list')
    else:
        form = BusinessParnterForm(instance=businesspartner)
    return render(request, 'crm/businesspartner_form.html', {'form': form, 'businesspartner': businesspartner})

@login_required
def businesspartner_delete(request, pk):
    businesspartner = get_object_or_404(BusinessPartner, pk=pk)
    if request.method == 'POST':
        businesspartner.delete()
        return redirect('crm:businesspartner_list')
    return render(request, 'crm/businesspartner_confirm_delete.html', {'businesspartner': businesspartner})

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