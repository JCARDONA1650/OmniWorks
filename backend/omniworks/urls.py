from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.core.urls')),
    path('api/', include('apps.notes.urls')),
    path('api/', include('apps.doc_generator.urls')),
    path('api/', include('apps.email_campaigns.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
