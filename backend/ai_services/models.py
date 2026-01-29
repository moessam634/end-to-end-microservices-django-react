from django.db import models
from django.contrib.auth import get_user_model
from users.models import MusicianProfile, VenueProfile
from gigs.models import Gig, GigApplication

User = get_user_model()

class AIService(models.Model):
    """Model to store AI-generated content and services"""
    
    CONTENT_TYPE_CHOICES = [
        ('musician_bio', 'Musician Bio'),
        ('venue_description', 'Venue Description'),
        ('gig_description', 'Gig Description'),
        ('setlist', 'Setlist'),
        ('cover_letter', 'Cover Letter'),
        ('marketing_copy', 'Marketing Copy'),
        ('proposal', 'Gig Proposal'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Basic information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_services')
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Input data for AI generation
    input_data = models.JSONField(default=dict)  # Data used to generate content
    prompt = models.TextField(blank=True)  # The actual prompt sent to AI
    
    # Generated content
    generated_content = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)  # Additional AI response data
    
    # Related objects (optional)
    musician_profile = models.ForeignKey(
        MusicianProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_generated_content'
    )
    venue_profile = models.ForeignKey(
        VenueProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_generated_content'
    )
    gig = models.ForeignKey(
        Gig, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_generated_content'
    )
    gig_application = models.ForeignKey(
        GigApplication, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_generated_content'
    )
    
    # AI service details
    ai_model = models.CharField(max_length=100, default='gpt-3.5-turbo')
    tokens_used = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'AI Service'
        verbose_name_plural = 'AI Services'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_content_type_display()} for {self.user.email} - {self.status}"

class AIRecommendation(models.Model):
    """Model to store AI-powered recommendations"""
    
    RECOMMENDATION_TYPE_CHOICES = [
        ('gig_match', 'Gig Match'),
        ('musician_match', 'Musician Match'),
        ('venue_match', 'Venue Match'),
        ('setlist_suggestion', 'Setlist Suggestion'),
        ('pricing_suggestion', 'Pricing Suggestion'),
    ]
    
    # Basic information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPE_CHOICES)
    
    # Recommendation data
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.FloatField(default=0.0)  # 0.0 to 1.0
    reasoning = models.TextField(blank=True)
    
    # Related objects
    recommended_gig = models.ForeignKey(
        Gig, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_recommendations'
    )
    recommended_musician = models.ForeignKey(
        MusicianProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_recommendations'
    )
    recommended_venue = models.ForeignKey(
        VenueProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_recommendations'
    )
    
    # User interaction
    is_viewed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    user_feedback = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'AI Recommendation'
        verbose_name_plural = 'AI Recommendations'
        ordering = ['-confidence_score', '-created_at']
    
    def __str__(self):
        return f"{self.get_recommendation_type_display()} - {self.title}"

class AITask(models.Model):
    """Model to track AI background tasks"""
    
    TASK_TYPE_CHOICES = [
        ('generate_bio', 'Generate Bio'),
        ('generate_setlist', 'Generate Setlist'),
        ('generate_proposal', 'Generate Proposal'),
        ('match_gigs', 'Match Gigs'),
        ('scan_external_platforms', 'Scan External Platforms'),
        ('generate_recommendations', 'Generate Recommendations'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Task information
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Celery task details
    celery_task_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Task data
    input_data = models.JSONField(default=dict)
    result_data = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    
    # Related objects
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_tasks')
    ai_service = models.ForeignKey(
        AIService, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='tasks'
    )
    
    # Progress tracking
    progress_percentage = models.PositiveIntegerField(default=0)
    estimated_completion = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'AI Task'
        verbose_name_plural = 'AI Tasks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_task_type_display()} - {self.status}"
