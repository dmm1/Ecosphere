# ecosphere/core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
from accounts.views import login_view, profile_view
from crm.views import dashboard

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', login_required(dashboard), name='dashboard'),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += i18n_patterns(
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/', login_required(profile_view), name='profile'),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('crm.urls', namespace='crm')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)