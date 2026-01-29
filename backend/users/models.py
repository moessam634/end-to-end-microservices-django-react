from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('musician', 'Musician'),
        ('venue', 'Venue Owner'),
        ('admin', 'Administrator'),
    ]
    
    # Basic fields
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='musician')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Profile fields
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Social media
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    user_notification_preferences = models.JSONField(default=dict, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def is_musician(self):
        return self.user_type == 'musician'
    
    @property
    def is_venue_owner(self):
        return self.user_type == 'venue'
    
    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

class MusicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='musician_profile')
    
    # Musical information
    primary_instrument = models.CharField(max_length=100)
    instruments = models.JSONField(default=list)  # List of instruments
    genres = models.JSONField(default=list)  # List of genres
    experience_years = models.PositiveIntegerField(default=0)
    
    # Performance details
    band_name = models.CharField(max_length=100, blank=True)
    is_solo_artist = models.BooleanField(default=False)
    band_size = models.PositiveIntegerField(default=1)
    
    # Repertoire
    setlist_examples = models.JSONField(default=list)  # List of songs
    original_music = models.BooleanField(default=False)
    cover_music = models.BooleanField(default=True)
    
    # Pricing
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    per_gig_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Availability
    availability_schedule = models.JSONField(default=dict)  # Weekly schedule
    travel_distance = models.PositiveIntegerField(default=50)  # miles
    
    # Portfolio
    portfolio_links = models.JSONField(default=list)  # List of URLs
    audio_samples = models.JSONField(default=list)  # List of audio file paths
    video_samples = models.JSONField(default=list)  # List of video file paths
    
    # AI-generated content
    ai_generated_bio = models.TextField(blank=True)
    ai_generated_setlist = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Musician Profile'
        verbose_name_plural = 'Musician Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.primary_instrument}"

class VenueProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='venue_profile')
    
    # Venue information
    venue_name = models.CharField(max_length=200)
    venue_type = models.CharField(max_length=100)  # Bar, Restaurant, Club, etc.
    capacity = models.PositiveIntegerField()
    
    # Location details
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Venue features
    has_stage = models.BooleanField(default=True)
    has_sound_system = models.BooleanField(default=True)
    has_lighting = models.BooleanField(default=True)
    has_parking = models.BooleanField(default=False)
    has_food = models.BooleanField(default=False)
    has_alcohol = models.BooleanField(default=False)
    
    # Musical preferences
    preferred_genres = models.JSONField(default=list)
    preferred_instruments = models.JSONField(default=list)
    
    # Booking information
    booking_lead_time = models.PositiveIntegerField(default=7)  # days
    payment_terms = models.CharField(max_length=200, blank=True)
    
    # Photos
    venue_photos = models.JSONField(default=list)  # List of image file paths
    
    # AI-generated content
    ai_generated_description = models.TextField(blank=True)
    ai_generated_marketing_copy = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Venue Profile'
        verbose_name_plural = 'Venue Profiles'
    
    def __str__(self):
        return self.venue_name
