# ecosphere/core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
from apps.accounts.views import login_view, profile_view
from crm.views import dashboard
from apps.organization.views import dashboard as org_dashboard


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', login_required(dashboard), name='dashboard'),
]

urlpatterns += i18n_patterns(
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/', login_required(profile_view), name='profile'),
    path('', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('crm.urls', 'crm'), namespace='crm')),
    path('organization/dashboard/', login_required(org_dashboard), name='org_dashboard'),
    path('', include(('apps.business_partner.urls', 'business_partner'), namespace='business_partner')),
    path('', include(('apps.tasks.urls', 'tasks'), namespace='tasks')),
    path('', include(('apps.contact.urls', 'contact'), namespace='contact')),
    path('api/', include(('apps.organization.urls', 'organization'), namespace='organization')),
    path('', include(('apps.organization.urls', 'organization'), namespace='organization')),
    path('search/', include(('apps.search.urls', 'search'), namespace='search')),
    path('profile/<int:user_id>/', include(('apps.organization.urls', 'organization'), namespace='organization')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
