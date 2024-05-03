from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Country, CountryAdmin, Group, Team

# Inline admin to show CountryAdmin in the User admin
class CountryAdminInline(admin.StackedInline):
    model = CountryAdmin
    can_delete = False
    verbose_name_plural = 'countries admin'

# Extend the existing User admin
class CustomUserAdmin(UserAdmin):
    inlines = (CountryAdminInline,)

# Unregister the original User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin for Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Country, CountryAdmin)

# Admin for Group
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_by')
    list_filter = ('permissions',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(country=request.user.countryadmin.country)

admin.site.register(Group, GroupAdmin)

# Admin for Team
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'created_by']
    list_filter = ['group__country']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group__country=request.user.countryadmin.country)

admin.site.register(Team, TeamAdmin)
