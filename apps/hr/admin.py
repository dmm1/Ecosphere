from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Department, Position

admin.site.register(Department)
admin.site.register(Position)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ('user', 'department', 'position')