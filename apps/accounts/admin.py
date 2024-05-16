from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email', 'phone_number']
    search_fields = ['user__username', 'user__email', 'phone_number']

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = 'user__email'  # Allows column order sorting
    get_email.short_description = 'Email Address'  # Renames column head

admin.site.register(UserProfile, UserProfileAdmin)

