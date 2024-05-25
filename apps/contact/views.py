from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.business_partner.models import BusinessPartner
from apps.contact.models import Contact
from .forms import ContactForm
from crm.models import Opportunity,  Lead
from apps.tasks.models import Task
from django.core.paginator import Paginator
from django.urls import reverse

@login_required
def contact_list(request):
    show_all = str(request.session.get('show_all', False)).lower()
    if 'show_all' in request.GET:
        show_all = str(request.GET.get('show_all', 'false')).lower() == 'true'
        request.session['show_all'] = show_all

    if show_all:
        contacts = Contact.objects.all().order_by('-created_at')
    else:
        contacts = Contact.objects.filter(user=request.user).order_by('-created_at')  # Only retrieve contacts assigned to the current user

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'apps/contact/contact_list.html', {'page_obj': page_obj, 'show_all': show_all})

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if form.cleaned_data['assign_to_me']:
                contact.user = request.user
            else:
                contact.user = None
            contact.save()
            return redirect('contact:contact_list')
    else:
        form = ContactForm()
    return render(request, 'apps/contact/contact_form.html', {'form': form})

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'apps/contact/contact_detail.html', {'contact': contact})

@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            if form.cleaned_data['assign_to_me']:
                contact.user = request.user
            else:
                contact.user = None
            contact.save()
            return redirect('contact:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'apps/contact/contact_form.html', {'form': form})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact:contact_list')
    return render(request, 'apps/contact/contact_confirm_delete.html', {'contact': contact})