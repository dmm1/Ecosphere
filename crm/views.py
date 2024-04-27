from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Opportunity,  Lead
from apps.tasks.models import Task
from .forms import OpportunityForm, LeadForm
from django.core.paginator import Paginator
from django.urls import reverse


@login_required
def dashboard(request):
    # Get the total number of opportunities for the user's business partners
    opportunities = Opportunity.objects.filter(assigned_to=request.user)
    total_opportunities = opportunities.count()
    open_opportunities = opportunities.filter(status='open').count()
    won_opportunities = opportunities.filter(status='won').count()

    # Get the total number of leads, new leads, and open leads for the user
    leads = Lead.objects.filter(user=request.user)
    total_leads = leads.count()
    new_leads = leads.filter(status='New').count()
    open_leads = leads.filter(status='Open').count()

    # Get the user's tasks
    user_tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')[:5]


    return render(request, 'dashboard.html', {
        'total_opportunities': total_opportunities,
        'open_opportunities': open_opportunities,
        'won_opportunities': won_opportunities,
        'total_leads': total_leads,
        'new_leads': new_leads,
        'open_leads': open_leads,
        'user_tasks': user_tasks,
    })


@login_required
def opportunity_list(request):
    show_all = str(request.session.get('show_all', False)).lower()
    if 'show_all' in request.GET:
        show_all = str(request.GET.get('show_all', 'false')).lower() == 'true'
        request.session['show_all'] = show_all

    if show_all:
        opportunities = Opportunity.objects.all().order_by('created_at')
    else:
        opportunities = Opportunity.objects.filter(assigned_to=request.user).order_by('created_at')

    paginator = Paginator(opportunities, 5)  # Show 5 opportunities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'crm/opportunity_list.html', {'page_obj': page_obj, 'show_all': show_all})
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



@login_required
def lead_list(request):
    show_all = str(request.session.get('show_all', False)).lower()
    if 'show_all' in request.GET:
        show_all = str(request.GET.get('show_all', 'false')).lower() == 'true'
        request.session['show_all'] = show_all

    if show_all:
        leads = Lead.objects.all().order_by('-created_at')
    else:
        leads = Lead.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(leads, 10)  # Show 10 leads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'crm/lead_list.html', {'page_obj': page_obj, 'show_all': show_all})


@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.user = request.user
            lead.save()

            # Get the last page of the paginated list
            leads = Lead.objects.filter(user=request.user)
            paginator = Paginator(leads, 10)  # Adjust the page size as needed
            last_page = paginator.num_pages
            return redirect(reverse('crm:lead_list') + f'?page={last_page}')
    else:
        form = LeadForm()
    return render(request, 'crm/lead_create.html', {'form': form})


@login_required
def lead_detail(request, pk):
    try:
        lead = Lead.objects.get(pk=pk, user=request.user)
    except Lead.DoesNotExist:
        return render(request, 'crm/lead_not_found.html', status=404)
    return render(request, 'crm/lead_detail.html', {'lead': lead})

@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('crm:lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)
    return render(request, 'crm/lead_update.html', {'form': form, 'lead': lead})
@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk, user=request.user)
    if request.method == 'POST':
        lead.delete()
        return redirect('crm:lead_list')
    return render(request, 'crm/lead_delete.html', {'lead': lead})

