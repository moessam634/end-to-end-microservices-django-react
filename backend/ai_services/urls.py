from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ai_services'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'services', views.AIServiceViewSet, basename='aiservice')
router.register(r'recommendations', views.AIRecommendationViewSet, basename='airecommendation')
router.register(r'tasks', views.AITaskViewSet, basename='aitask')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional endpoints
    path('generate-content/', views.AIContentGenerationView.as_view(), name='generate_content'),
    path('match-gigs/', views.AIGigMatchingView.as_view(), name='match_gigs'),
]
