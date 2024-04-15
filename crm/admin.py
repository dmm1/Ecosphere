from django.contrib import admin
from django.contrib.auth.models import User
from .models import Customer, Opportunity

class OpportunityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer)
admin.site.register(Opportunity, OpportunityAdmin)
