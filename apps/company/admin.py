from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Department, Position, Team

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Team)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass