from rest_framework import serializers
from .models import Notification, NotificationTemplate, NotificationPreference, NotificationLog
from users.serializers import MusicianProfileSerializer, VenueProfileSerializer
from gigs.serializers import GigSerializer, GigApplicationSerializer

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    gig = GigSerializer(read_only=True)
    gig_application = GigApplicationSerializer(read_only=True)
    musician_profile = MusicianProfileSerializer(read_only=True)
    venue_profile = VenueProfileSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'notification_type', 'priority', 'title', 'message',
            'action_url', 'gig', 'gig_application', 'musician_profile',
            'venue_profile', 'is_read', 'is_sent', 'read_at', 'email_sent',
            'sms_sent', 'push_sent', 'created_at', 'scheduled_for'
        ]
        read_only_fields = [
            'id', 'user', 'is_sent', 'read_at', 'email_sent', 'sms_sent',
            'push_sent', 'created_at'
        ]

class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    
    class Meta:
        model = Notification
        fields = [
            'notification_type', 'priority', 'title', 'message', 'action_url',
            'gig', 'gig_application', 'musician_profile', 'venue_profile',
            'scheduled_for'
        ]
    
    def validate(self, data):
        """Validate notification creation"""
        notification_type = data.get('notification_type')
        
        # Validate that appropriate related objects are provided based on type
        if notification_type in ['gig_created', 'gig_updated', 'gig_cancelled']:
            if not data.get('gig'):
                raise serializers.ValidationError(
                    "Gig is required for gig-related notifications"
                )
        elif notification_type in ['application_received', 'application_accepted', 'application_rejected']:
            if not data.get('gig_application'):
                raise serializers.ValidationError(
                    "Gig application is required for application-related notifications"
                )
        
        return data

class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notifications (marking as read, etc.)"""
    
    class Meta:
        model = Notification
        fields = ['is_read', 'read_at']
    
    def update(self, instance, validated_data):
        """Update notification and set read_at timestamp"""
        if validated_data.get('is_read') and not instance.is_read:
            from django.utils import timezone
            validated_data['read_at'] = timezone.now()
        
        return super().update(instance, validated_data)

class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer for Notification Template model"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'template_type', 'notification_type', 'subject',
            'body', 'available_variables', 'is_active', 'is_default',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for Notification Preference model"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'notification_type', 'is_enabled', 'delivery_methods',
            'frequency', 'quiet_hours_start', 'quiet_hours_end', 'timezone',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class NotificationPreferenceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notification preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'is_enabled', 'delivery_methods', 'frequency', 'quiet_hours_start',
            'quiet_hours_end', 'timezone'
        ]

class NotificationLogSerializer(serializers.ModelSerializer):
    """Serializer for Notification Log model"""
    
    notification = NotificationSerializer(read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification', 'delivery_method', 'status', 'external_id',
            'error_message', 'attempted_at', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'notification', 'status', 'external_id', 'error_message',
            'attempted_at', 'delivered_at'
        ]
