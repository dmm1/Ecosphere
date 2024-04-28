from django.http import JsonResponse
from django.db.models import Q
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from apps.contact.models import Contact
from apps.business_partner.models import BusinessPartner
from apps.tasks.models import Task
from crm.models import Lead
from crm.models import Opportunity
from .forms import SearchForm

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['q']
        contacts = Contact.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        business_partners = BusinessPartner.objects.filter(Q(name__icontains=query))
        tasks = Task.objects.filter(Q(title__icontains=query))
        leads = Lead.objects.filter(Q(name__icontains=query))
        opportunities = Opportunity.objects.filter(Q(name__icontains=query))

        return render(request, 'apps/search/search_results.html', {
            'contacts': contacts,
            'business_partners': business_partners,
            'tasks': tasks,
            'leads': leads,
            'opportunities': opportunities,
            'form': form
        })
    else:
        return render(request, 'apps/search/search_results.html', {'form': form})

import logging

def autocomplete(request):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    query = request.GET.get('q', '')
    models = request.GET.getlist('models', [])
    logger.info(f"Autocomplete request: q={query}, models={models}")
    results = []

    for model in models:
        model_class = apps.get_model(model)
        model_data = list(model_class.objects.filter(Q(name__icontains=query)).values('id', 'name'))
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
