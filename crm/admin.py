from django.contrib import admin
from django.contrib.auth.models import User
from .models import BusinessPartner, Opportunity

class OpportunityAdmin(admin.ModelAdmin):
    pass

admin.site.register(BusinessPartner)
admin.site.register(Opportunity, OpportunityAdmin)
