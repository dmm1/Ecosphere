from django.contrib import admin
from django.contrib.auth.models import User
from .models import BusinessPartner, Opportunity, Lead, Contact

class OpportunityAdmin(admin.ModelAdmin):
    pass

admin.site.register(BusinessPartner)
admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Lead)
admin.site.register(Contact)
