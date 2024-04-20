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
]

urlpatterns += i18n_patterns(
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/', login_required(profile_view), name='profile'),
    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('crm.urls', 'crm'), namespace='crm')),
    path('', include(('tasks.urls', 'tasks'), namespace='tasks')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
