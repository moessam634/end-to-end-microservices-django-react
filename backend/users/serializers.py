from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MusicianProfile, VenueProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'user_type',
            'phone_number', 'bio', 'profile_picture', 'date_of_birth',
            'city', 'state', 'country', 'website', 'instagram', 'facebook',
            'twitter', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'password',
            'password_confirm', 'user_type', 'phone_number', 'city', 'state', 'country'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'user_type',
            'phone_number', 'bio', 'profile_picture', 'date_of_birth',
            'city', 'state', 'country', 'website', 'instagram', 'facebook',
            'twitter', 'is_verified', 'user_notification_preferences'
        ]
        read_only_fields = ['id', 'email', 'user_type', 'is_verified']

class MusicianProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MusicianProfile
        fields = [
            'id', 'user', 'primary_instrument', 'instruments', 'genres',
            'experience_years', 'band_name', 'is_solo_artist', 'band_size',
            'setlist_examples', 'original_music', 'cover_music', 'hourly_rate',
            'per_gig_rate', 'availability_schedule', 'travel_distance',
            'portfolio_links', 'audio_samples', 'video_samples',
            'ai_generated_bio', 'ai_generated_setlist', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class VenueProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = VenueProfile
        fields = [
            'id', 'user', 'venue_name', 'venue_type', 'capacity', 'address',
            'latitude', 'longitude', 'has_stage', 'has_sound_system',
            'has_lighting', 'has_parking', 'has_food', 'has_alcohol',
            'preferred_genres', 'preferred_instruments', 'booking_lead_time',
            'payment_terms', 'venue_photos', 'ai_generated_description',
            'ai_generated_marketing_copy', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class UserDetailSerializer(serializers.ModelSerializer):
    musician_profile = MusicianProfileSerializer(read_only=True)
    venue_profile = VenueProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'user_type',
            'phone_number', 'bio', 'profile_picture', 'date_of_birth',
            'city', 'state', 'country', 'website', 'instagram', 'facebook',
            'twitter', 'is_verified', 'user_notification_preferences',
            'musician_profile', 'venue_profile', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
