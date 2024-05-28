# ecosphere/core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
from apps.accounts.views import login_view, profile_view
from crm.views import dashboard
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', login_required(dashboard), name='dashboard'),
]

urlpatterns += i18n_patterns(
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/', login_required(profile_view), name='profile'),
    path('', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('crm.urls', 'crm'), namespace='crm')),
    path('', include(('apps.business_partner.urls', 'business_partner'), namespace='business_partner')),
    path('', include(('apps.tasks.urls', 'tasks'), namespace='tasks')),
    path('', include(('apps.contact.urls', 'contact'), namespace='contact')),
    path('search/', include(('apps.search.urls', 'search'), namespace='search')),
    path('company/', include(('apps.company.urls', 'company'), namespace='company')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
