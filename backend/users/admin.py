from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, MusicianProfile, VenueProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_verified', 'city', 'country', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'date_joined', 'country', 'city')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'city', 'country')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type', 'phone_number', 'bio', 'profile_picture', 'date_of_birth')}),
        ('Location', {'fields': ('city', 'state', 'country')}),
        ('Social Media', {'fields': ('website', 'instagram', 'facebook', 'twitter')}),
        ('Verification', {'fields': ('is_verified', 'verification_date')}),
        ('Preferences', {'fields': ('user_notification_preferences',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type'),
        }),
    )
    
    readonly_fields = ('verification_date', 'date_joined', 'last_login')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('musician_profile', 'venue_profile')

@admin.register(MusicianProfile)
class MusicianProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'primary_instrument', 'genres_display', 'experience_years', 'band_name', 'hourly_rate', 'city')
    list_filter = ('primary_instrument', 'experience_years', 'original_music', 'cover_music', 'user__city')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'primary_instrument', 'band_name')
    ordering = ('user__first_name',)
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Musical Information', {'fields': ('primary_instrument', 'instruments', 'genres', 'experience_years')}),
        ('Performance Details', {'fields': ('band_name', 'is_solo_artist', 'band_size')}),
        ('Repertoire', {'fields': ('setlist_examples', 'original_music', 'cover_music')}),
        ('Pricing', {'fields': ('hourly_rate', 'per_gig_rate')}),
        ('Availability', {'fields': ('availability_schedule', 'travel_distance')}),
        ('Portfolio', {'fields': ('portfolio_links', 'audio_samples', 'video_samples')}),
        ('AI Generated Content', {'fields': ('ai_generated_bio', 'ai_generated_setlist')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def genres_display(self, obj):
        if obj.genres:
            return ', '.join(obj.genres[:3]) + ('...' if len(obj.genres) > 3 else '')
        return '-'
    genres_display.short_description = 'Genres'
    
    def city(self, obj):
        return obj.user.city
    city.short_description = 'City'

@admin.register(VenueProfile)
class VenueProfileAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'user', 'venue_type', 'capacity', 'city', 'has_stage', 'has_sound_system', 'booking_lead_time')
    list_filter = ('venue_type', 'has_stage', 'has_sound_system', 'has_lighting', 'has_parking', 'has_food', 'has_alcohol', 'user__city')
    search_fields = ('venue_name', 'user__email', 'user__first_name', 'user__last_name', 'address')
    ordering = ('venue_name',)
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Venue Information', {'fields': ('venue_name', 'venue_type', 'capacity')}),
        ('Location', {'fields': ('address', 'latitude', 'longitude')}),
        ('Features', {'fields': ('has_stage', 'has_sound_system', 'has_lighting', 'has_parking', 'has_food', 'has_alcohol')}),
        ('Musical Preferences', {'fields': ('preferred_genres', 'preferred_instruments')}),
        ('Booking Information', {'fields': ('booking_lead_time', 'payment_terms')}),
        ('Photos', {'fields': ('venue_photos',)}),
        ('AI Generated Content', {'fields': ('ai_generated_description', 'ai_generated_marketing_copy')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def city(self, obj):
        return obj.user.city
    city.short_description = 'City'
