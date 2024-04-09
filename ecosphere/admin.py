from django.contrib import admin

from .models import Customer  # import your model


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('bid', 'name', 'date_of_creation', 'Potential')
    list_filters = ['name']


admin.site.register(Customer, CustomerAdmin)
# Register your models here.
