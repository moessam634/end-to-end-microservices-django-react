from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('auth/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    
    # Musician specific endpoints
    path('musician/profile/', views.MusicianProfileView.as_view(), name='musician_profile'),
    path('musician/profile/update/', views.MusicianProfileUpdateView.as_view(), name='musician_profile_update'),
    
    # Venue specific endpoints
    path('venue/profile/', views.VenueProfileView.as_view(), name='venue_profile'),
    path('venue/profile/update/', views.VenueProfileUpdateView.as_view(), name='venue_profile_update'),
    
    # User management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]
