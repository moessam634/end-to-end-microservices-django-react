from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import health_views

urlpatterns = [
    # Health check endpoints
    path('health/', health_views.health_check, name='health_check'),
    path('health/ready/', health_views.readiness_check, name='readiness_check'),
    path('health/live/', health_views.liveness_check, name='liveness_check'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API endpoints
    path('api/', include('users.urls')),
    path('api/', include('gigs.urls')),
    path('api/', include('venues.urls')),
    path('api/', include('ai_services.urls')),
    path('api/', include('notifications.urls')),
    
    # Authentication
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Gig Router Administration"
admin.site.site_title = "Gig Router Admin"
admin.site.index_title = "Welcome to Gig Router Admin"
