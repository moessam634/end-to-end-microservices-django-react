from django.db import models
from django.contrib.auth import get_user_model
from users.models import MusicianProfile, VenueProfile
from gigs.models import Gig, GigApplication

User = get_user_model()

class Notification(models.Model):
    """Model for storing user notifications"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('gig_created', 'New Gig Available'),
        ('gig_updated', 'Gig Updated'),
        ('gig_cancelled', 'Gig Cancelled'),
        ('application_received', 'Application Received'),
        ('application_accepted', 'Application Accepted'),
        ('application_rejected', 'Application Rejected'),
        ('gig_reminder', 'Gig Reminder'),
        ('payment_due', 'Payment Due'),
        ('profile_verification', 'Profile Verification'),
        ('ai_content_ready', 'AI Content Ready'),
        ('recommendation', 'New Recommendation'),
        ('system_message', 'System Message'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    action_url = models.URLField(blank=True)  # URL to navigate to when clicked
    
    # Related objects (optional)
    gig = models.ForeignKey(
        Gig, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    gig_application = models.ForeignKey(
        GigApplication, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    musician_profile = models.ForeignKey(
        MusicianProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    venue_profile = models.ForeignKey(
        VenueProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    
    # Status and interaction
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery methods
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)  # For delayed notifications
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"

class NotificationTemplate(models.Model):
    """Model for storing notification templates"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
    ]
    
    # Template information
    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    notification_type = models.CharField(max_length=50, choices=Notification.NOTIFICATION_TYPE_CHOICES)
    
    # Template content
    subject = models.CharField(max_length=200, blank=True)  # For email
    body = models.TextField()
    
    # Template variables (JSON field with available variables)
    available_variables = models.JSONField(default=list)
    
    # Settings
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
        unique_together = ['template_type', 'notification_type']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

class NotificationPreference(models.Model):
    """Model for storing user notification preferences"""
    
    DELIVERY_METHOD_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Only'),
    ]
    
    # User and notification type
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notification_settings')
    notification_type = models.CharField(max_length=50, choices=Notification.NOTIFICATION_TYPE_CHOICES)
    
    # Preferences
    is_enabled = models.BooleanField(default=True)
    delivery_methods = models.JSONField(default=list)  # List of preferred delivery methods
    frequency = models.CharField(max_length=20, default='immediate')  # immediate, daily, weekly
    
    # Timing preferences
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
        unique_together = ['user', 'notification_type']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_notification_type_display()}"

class NotificationLog(models.Model):
    """Model for logging notification delivery attempts"""
    
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('unsubscribed', 'Unsubscribed'),
    ]
    
    # Related notification
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='delivery_logs')
    
    # Delivery details
    delivery_method = models.CharField(max_length=20, choices=NotificationTemplate.TEMPLATE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    
    # External service details
    external_id = models.CharField(max_length=255, blank=True)  # ID from email/SMS service
    error_message = models.TextField(blank=True)
    
    # Timestamps
    attempted_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.notification.title} - {self.get_delivery_method_display()} - {self.status}"
