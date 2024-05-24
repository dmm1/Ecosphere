from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email', 'get_phone_number']
    search_fields = ['user__username', 'user__email', 'employee__phone_number']

    def get_email(self, obj):
        return obj.user.email

    def get_phone_number(self, obj):
        return obj.employee.phone_number
    get_phone_number.admin_order_field = 'employee__phone_number'  # Allows column order sorting
    get_phone_number.short_description = 'Phone Number'  # Renames column head

    get_email.admin_order_field = 'user__email'  # Allows column order sorting
    get_email.short_description = 'Email Address'  # Renames column head

admin.site.register(UserProfile, UserProfileAdmin)

