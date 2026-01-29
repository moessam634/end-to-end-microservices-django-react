from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User, MusicianProfile, VenueProfile

class Gig(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    GENRE_CHOICES = [
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('jazz', 'Jazz'),
        ('blues', 'Blues'),
        ('country', 'Country'),
        ('electronic', 'Electronic'),
        ('hip_hop', 'Hip Hop'),
        ('classical', 'Classical'),
        ('folk', 'Folk'),
        ('reggae', 'Reggae'),
        ('other', 'Other'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.ForeignKey(VenueProfile, on_delete=models.CASCADE, related_name='gigs')
    
    # Event details
    event_date = models.DateTimeField()
    duration_hours = models.PositiveIntegerField(default=2)
    setup_time = models.PositiveIntegerField(default=30)  # minutes
    
    # Musical requirements
    genres = models.JSONField(default=list)  # List of genres
    instruments_needed = models.JSONField(default=list)  # List of instruments
    band_size_min = models.PositiveIntegerField(default=1)
    band_size_max = models.PositiveIntegerField(default=5)
    
    # Compensation
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=[
        ('per_gig', 'Per Gig'),
        ('per_hour', 'Per Hour'),
        ('negotiable', 'Negotiable'),
    ])
    
    # Requirements and preferences
    experience_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('professional', 'Professional'),
    ])
    original_music_required = models.BooleanField(default=False)
    cover_music_required = models.BooleanField(default=True)
    
    # Venue features available
    sound_system_provided = models.BooleanField(default=True)
    lighting_provided = models.BooleanField(default=True)
    backline_provided = models.BooleanField(default=False)
    
    # Additional information
    special_requirements = models.TextField(blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    
    # Status and management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_featured = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    
    # AI-generated content
    ai_generated_description = models.TextField(blank=True)
    ai_generated_marketing_copy = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Gig'
        verbose_name_plural = 'Gigs'
        ordering = ['-event_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.venue.venue_name} - {self.event_date.strftime('%B %d, %Y')}"
    
    @property
    def is_open_for_applications(self):
        return self.status == 'open' and (not self.deadline or self.deadline > timezone.now())
    
    @property
    def days_until_event(self):
        delta = self.event_date - timezone.now()
        return delta.days

class GigApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='applications')
    musician = models.ForeignKey(MusicianProfile, on_delete=models.CASCADE, related_name='gig_applications')
    
    # Application details
    cover_letter = models.TextField()
    proposed_setlist = models.JSONField(default=list)
    proposed_duration = models.PositiveIntegerField(default=2)  # hours
    proposed_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Supporting materials
    portfolio_links = models.JSONField(default=list)
    audio_samples = models.JSONField(default=list)
    video_samples = models.JSONField(default=list)
    
    # Status and communication
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    venue_notes = models.TextField(blank=True)
    musician_notes = models.TextField(blank=True)
    
    # AI-generated content
    ai_generated_cover_letter = models.TextField(blank=True)
    ai_generated_setlist = models.JSONField(default=list)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Gig Application'
        verbose_name_plural = 'Gig Applications'
        unique_together = ['gig', 'musician']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.musician.user.get_full_name()} - {self.gig.title}"
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_accepted(self):
        return self.status == 'accepted'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
