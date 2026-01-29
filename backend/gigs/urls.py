from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'gigs'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'gigs', views.GigViewSet, basename='gig')
router.register(r'applications', views.GigApplicationViewSet, basename='gigapplication')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional endpoints
    path('search/', views.GigSearchView.as_view(), name='gig_search'),
    path('my-gigs/', views.MyGigsView.as_view(), name='my_gigs'),
]
