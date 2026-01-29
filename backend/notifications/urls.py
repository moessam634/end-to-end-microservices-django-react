from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'notifications'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'preferences', views.NotificationPreferenceViewSet, basename='notificationpreference')
router.register(r'templates', views.NotificationTemplateViewSet, basename='notificationtemplate')
router.register(r'logs', views.NotificationLogViewSet, basename='notificationlog')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional endpoints
    path('stats/', views.NotificationStatsView.as_view(), name='notification_stats'),
    path('test/', views.NotificationTestView.as_view(), name='test_notification'),
]
