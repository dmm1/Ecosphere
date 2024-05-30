from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Department, Position, Team, Company 

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Company)  

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass