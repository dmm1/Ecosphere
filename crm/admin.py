from django.contrib import admin
from django.contrib.auth.models import User
from .models import Opportunity, Lead

class OpportunityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Lead)

