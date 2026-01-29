from rest_framework import serializers
from .models import AIService, AIRecommendation, AITask
from users.serializers import MusicianProfileSerializer, VenueProfileSerializer
from gigs.serializers import GigSerializer, GigApplicationSerializer

class AIServiceSerializer(serializers.ModelSerializer):
    """Serializer for AI Service model"""
    
    class Meta:
        model = AIService
        fields = [
            'id', 'user', 'content_type', 'status', 'input_data', 'prompt',
            'generated_content', 'metadata', 'musician_profile', 'venue_profile',
            'gig', 'gig_application', 'ai_model', 'tokens_used', 'cost',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'generated_content', 'metadata',
            'tokens_used', 'cost', 'created_at', 'updated_at', 'completed_at'
        ]

class AIServiceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating AI Service requests"""
    
    class Meta:
        model = AIService
        fields = [
            'content_type', 'input_data', 'prompt', 'musician_profile',
            'venue_profile', 'gig', 'gig_application', 'ai_model'
        ]
    
    def validate(self, data):
        """Validate that at least one related object is provided"""
        related_objects = [
            data.get('musician_profile'),
            data.get('venue_profile'),
            data.get('gig'),
            data.get('gig_application')
        ]
        
        if not any(related_objects):
            raise serializers.ValidationError(
                "At least one related object (musician_profile, venue_profile, gig, or gig_application) must be provided."
            )
        
        return data

class AIRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for AI Recommendation model"""
    
    recommended_gig = GigSerializer(read_only=True)
    recommended_musician = MusicianProfileSerializer(read_only=True)
    recommended_venue = VenueProfileSerializer(read_only=True)
    
    class Meta:
        model = AIRecommendation
        fields = [
            'id', 'user', 'recommendation_type', 'title', 'description',
            'confidence_score', 'reasoning', 'recommended_gig',
            'recommended_musician', 'recommended_venue', 'is_viewed',
            'is_accepted', 'user_feedback', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'confidence_score', 'reasoning', 'is_viewed',
            'is_accepted', 'user_feedback', 'created_at', 'updated_at'
        ]

class AIRecommendationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating AI Recommendation (feedback)"""
    
    class Meta:
        model = AIRecommendation
        fields = ['is_viewed', 'is_accepted', 'user_feedback']

class AITaskSerializer(serializers.ModelSerializer):
    """Serializer for AI Task model"""
    
    class Meta:
        model = AITask
        fields = [
            'id', 'task_type', 'status', 'celery_task_id', 'input_data',
            'result_data', 'error_message', 'user', 'ai_service',
            'progress_percentage', 'estimated_completion', 'created_at',
            'started_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'status', 'celery_task_id', 'result_data', 'error_message',
            'progress_percentage', 'estimated_completion', 'created_at',
            'started_at', 'completed_at'
        ]

class AITaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating AI Task requests"""
    
    class Meta:
        model = AITask
        fields = ['task_type', 'input_data', 'ai_service']
    
    def validate(self, data):
        """Validate task creation"""
        task_type = data.get('task_type')
        input_data = data.get('input_data', {})
        
        # Add validation based on task type
        if task_type == 'generate_bio' and not input_data.get('musician_profile_id'):
            raise serializers.ValidationError(
                "musician_profile_id is required for generate_bio task"
            )
        
        return data
