from django.http import JsonResponse
from django.db.models import Q
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from apps.contact.models import Contact
from apps.business_partner.models import BusinessPartner
from apps.tasks.models import Task
from crm.models import Lead
from crm.models import Opportunity
from apps.company.models import Employee, Department, Position, Team
from .forms import SearchForm

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['q']
        words = query.split()

        contacts = Contact.objects.none()
        employees = Employee.objects.none()
        for word in words:
            contacts |= Contact.objects.filter(Q(first_name__icontains=word) | Q(last_name__icontains=word))
            employees |= Employee.objects.filter(Q(user__first_name__icontains=word) | Q(user__last_name__icontains=word))

        business_partners = BusinessPartner.objects.filter(Q(name__icontains=query))
        tasks = Task.objects.filter(Q(title__icontains=query))
        leads = Lead.objects.filter(Q(name__icontains=query))
        opportunities = Opportunity.objects.filter(Q(name__icontains=query))
        departments = Department.objects.filter(Q(name__icontains=query))
        teams = Team.objects.filter(Q(title__icontains=query))
        positions = Position.objects.filter(Q(title__icontains=query))

        return render(request, 'apps/search/search_results.html', {
            'contacts': contacts,
            'business_partners': business_partners,
            'tasks': tasks,
            'leads': leads,
            'opportunities': opportunities,
            'employees': employees,
            'departments': departments,
            'positions': positions,
            'teams': teams,
            'form': form
        })
    else:
        return render(request, 'apps/search/search_results.html', {'form': form})

import logging

def autocomplete(request):
    q = request.GET.get('q', '').lower() 
    if len(q) < 3:
        return JsonResponse({'results': []})

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    models = request.GET.get('models', '').split(',')
    results = []
    logger.info(f"Autocomplete request: q={q}, models={models}")

    name_fields_mapping = {
        'contact.Contact': ['first_name', 'last_name'],
        'business_partner.BusinessPartner': ['name'],
        'company.Employee': ['user__first_name', 'user__last_name'],
   

        # Add other models and their name fields here
    }

    for model in models:
        app_label, model_name = model.rsplit('.', 1)
        model_class = apps.get_model(app_label, model_name)
        name_fields = name_fields_mapping.get(model, ['name'])
        query = Q()
        for name_field in name_fields:
            query |= Q(**{f'{name_field}__icontains': q})
        model_data = list(model_class.objects.filter(query).values('id', *name_fields))
        results.extend(model_data)

    logger.info(f"Autocomplete results: {results}")
    return JsonResponse({'results': results})

def search_results(request):
    query = request.GET.get('q', '')
    model_name = request.GET.get('model', '')
    if model_name:
        model_class = apps.get_model(model_name)
        model_data = list(model_class.objects.filter(Q(name__icontains=query)).values('id', 'name'))
        return render(request, 'search_results.html', {model_name.lower(): model_data})
    else:
        return render(request, 'apps/search/search_results.html', {})
