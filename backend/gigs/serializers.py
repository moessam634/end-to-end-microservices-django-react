from rest_framework import serializers
from .models import Gig, GigApplication
from users.serializers import MusicianProfileSerializer, VenueProfileSerializer
from django.utils import timezone

class GigSerializer(serializers.ModelSerializer):
    """Serializer for Gig model"""
    
    venue = VenueProfileSerializer(read_only=True)
    venue_id = serializers.IntegerField(write_only=True)
    applications_count = serializers.SerializerMethodField()
    days_until_event = serializers.SerializerMethodField()
    is_open_for_applications = serializers.SerializerMethodField()
    
    class Meta:
        model = Gig
        fields = [
            'id', 'title', 'description', 'venue', 'venue_id', 'event_date',
            'duration_hours', 'setup_time', 'genres', 'instruments_needed',
            'band_size_min', 'band_size_max', 'payment_amount', 'payment_type',
            'experience_level', 'original_music_required', 'cover_music_required',
            'sound_system_provided', 'lighting_provided', 'backline_provided',
            'special_requirements', 'contact_person', 'contact_phone',
            'contact_email', 'status', 'is_featured', 'is_urgent',
            'ai_generated_description', 'ai_generated_marketing_copy',
            'created_at', 'updated_at', 'deadline', 'applications_count',
            'days_until_event', 'is_open_for_applications'
        ]
        read_only_fields = [
            'id', 'venue', 'ai_generated_description', 'ai_generated_marketing_copy',
            'created_at', 'updated_at', 'applications_count', 'days_until_event',
            'is_open_for_applications'
        ]
    
    def get_applications_count(self, obj):
        """Get the number of applications for this gig"""
        return obj.applications.count()
    
    def get_days_until_event(self, obj):
        """Get days until the event"""
        return obj.days_until_event
    
    def get_is_open_for_applications(self, obj):
        """Check if gig is open for applications"""
        return obj.is_open_for_applications
    
    def validate_event_date(self, value):
        """Validate that event date is in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value
    
    def validate_deadline(self, value):
        """Validate that deadline is before event date"""
        if value and 'event_date' in self.initial_data:
            event_date = timezone.datetime.fromisoformat(
                self.initial_data['event_date'].replace('Z', '+00:00')
            )
            if value >= event_date:
                raise serializers.ValidationError(
                    "Application deadline must be before the event date."
                )
        return value

class GigCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating gigs"""
    
    class Meta:
        model = Gig
        fields = [
            'title', 'description', 'venue_id', 'event_date', 'duration_hours',
            'setup_time', 'genres', 'instruments_needed', 'band_size_min',
            'band_size_max', 'payment_amount', 'payment_type', 'experience_level',
            'original_music_required', 'cover_music_required', 'sound_system_provided',
            'lighting_provided', 'backline_provided', 'special_requirements',
            'contact_person', 'contact_phone', 'contact_email', 'is_featured',
            'is_urgent', 'deadline'
        ]
    
    def validate_venue_id(self, value):
        """Validate that the venue exists and belongs to the user"""
        from users.models import VenueProfile
        try:
            venue = VenueProfile.objects.get(id=value)
            if venue.user != self.context['request'].user:
                raise serializers.ValidationError(
                    "You can only create gigs for your own venues."
                )
        except VenueProfile.DoesNotExist:
            raise serializers.ValidationError("Venue not found.")
        return value

class GigApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Gig Application model"""
    
    gig = GigSerializer(read_only=True)
    gig_id = serializers.IntegerField(write_only=True)
    musician = MusicianProfileSerializer(read_only=True)
    musician_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GigApplication
        fields = [
            'id', 'gig', 'gig_id', 'musician', 'musician_id', 'cover_letter',
            'proposed_setlist', 'proposed_duration', 'proposed_rate',
            'portfolio_links', 'audio_samples', 'video_samples', 'status',
            'venue_notes', 'musician_notes', 'ai_generated_cover_letter',
            'ai_generated_setlist', 'applied_at', 'updated_at', 'responded_at'
        ]
        read_only_fields = [
            'id', 'gig', 'musician', 'status', 'venue_notes', 'musician_notes',
            'ai_generated_cover_letter', 'ai_generated_setlist', 'applied_at',
            'updated_at', 'responded_at'
        ]
    
    def validate_gig_id(self, value):
        """Validate that the gig exists and is open for applications"""
        from .models import Gig
        try:
            gig = Gig.objects.get(id=value)
            if not gig.is_open_for_applications:
                raise serializers.ValidationError(
                    "This gig is not currently accepting applications."
                )
        except Gig.DoesNotExist:
            raise serializers.ValidationError("Gig not found.")
        return value
    
    def validate_musician_id(self, value):
        """Validate that the musician profile belongs to the user"""
        from users.models import MusicianProfile
        try:
            musician = MusicianProfile.objects.get(id=value)
            if musician.user != self.context['request'].user:
                raise serializers.ValidationError(
                    "You can only apply with your own musician profile."
                )
        except MusicianProfile.DoesNotExist:
            raise serializers.ValidationError("Musician profile not found.")
        return value
    
    def validate(self, data):
        """Validate the application"""
        gig_id = data.get('gig_id')
        musician_id = data.get('musician_id')
        
        # Check if user already applied to this gig
        if gig_id and musician_id:
            existing_application = GigApplication.objects.filter(
                gig_id=gig_id, musician_id=musician_id
            ).exists()
            if existing_application:
                raise serializers.ValidationError(
                    "You have already applied to this gig."
                )
        
        return data

class GigApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating gig applications"""
    
    class Meta:
        model = GigApplication
        fields = [
            'gig_id', 'musician_id', 'cover_letter', 'proposed_setlist',
            'proposed_duration', 'proposed_rate', 'portfolio_links',
            'audio_samples', 'video_samples'
        ]

class GigApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating gig applications (venue response)"""
    
    class Meta:
        model = GigApplication
        fields = ['status', 'venue_notes']
    
    def validate_status(self, value):
        """Validate status change"""
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError(
                "Status must be either 'accepted' or 'rejected'."
            )
        return value
    
    def update(self, instance, validated_data):
        """Update application and set responded_at timestamp"""
        if 'status' in validated_data and instance.status == 'pending':
            validated_data['responded_at'] = timezone.now()
        
        return super().update(instance, validated_data)
