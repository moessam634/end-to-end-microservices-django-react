from django.contrib import admin
from .models import Gig, GigApplication

@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'venue', 'event_date', 'status', 'payment_amount',
        'experience_level', 'is_featured', 'is_urgent', 'created_at'
    ]
    list_filter = [
        'status', 'experience_level', 'payment_type', 'is_featured',
        'is_urgent', 'event_date', 'created_at'
    ]
    search_fields = ['title', 'description', 'venue__venue_name', 'contact_person']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-event_date', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'venue', 'event_date', 'duration_hours', 'setup_time')
        }),
        ('Musical Requirements', {
            'fields': ('genres', 'instruments_needed', 'band_size_min', 'band_size_max', 'experience_level')
        }),
        ('Music Preferences', {
            'fields': ('original_music_required', 'cover_music_required')
        }),
        ('Compensation', {
            'fields': ('payment_amount', 'payment_type')
        }),
        ('Venue Features', {
            'fields': ('sound_system_provided', 'lighting_provided', 'backline_provided')
        }),
        ('Additional Information', {
            'fields': ('special_requirements', 'contact_person', 'contact_phone', 'contact_email')
        }),
        ('Status & Management', {
            'fields': ('status', 'is_featured', 'is_urgent', 'deadline')
        }),
        ('AI Generated Content', {
            'fields': ('ai_generated_description', 'ai_generated_marketing_copy'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_urgent', 'close_gigs']
    
    def mark_as_featured(self, request, queryset):
        """Mark selected gigs as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} gigs marked as featured.')
    mark_as_featured.short_description = "Mark selected gigs as featured"
    
    def mark_as_urgent(self, request, queryset):
        """Mark selected gigs as urgent"""
        updated = queryset.update(is_urgent=True)
        self.message_user(request, f'{updated} gigs marked as urgent.')
    mark_as_urgent.short_description = "Mark selected gigs as urgent"
    
    def close_gigs(self, request, queryset):
        """Close selected gigs"""
        updated = queryset.filter(status='open').update(status='pending')
        self.message_user(request, f'{updated} gigs closed.')
    close_gigs.short_description = "Close selected gigs"

@admin.register(GigApplication)
class GigApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'musician', 'gig', 'status', 'proposed_rate',
        'applied_at', 'responded_at'
    ]
    list_filter = ['status', 'applied_at', 'responded_at']
    search_fields = [
        'musician__user__email', 'gig__title', 'cover_letter',
        'venue_notes', 'musician_notes'
    ]
    readonly_fields = ['applied_at', 'updated_at', 'responded_at']
    ordering = ['-applied_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('gig', 'musician', 'status')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'proposed_setlist', 'proposed_duration', 'proposed_rate')
        }),
        ('Supporting Materials', {
            'fields': ('portfolio_links', 'audio_samples', 'video_samples'),
            'classes': ('collapse',)
        }),
        ('Communication', {
            'fields': ('venue_notes', 'musician_notes')
        }),
        ('AI Generated Content', {
            'fields': ('ai_generated_cover_letter', 'ai_generated_setlist'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at', 'responded_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['accept_applications', 'reject_applications']
    
    def accept_applications(self, request, queryset):
        """Accept selected applications"""
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='accepted',
            responded_at=timezone.now()
        )
        self.message_user(request, f'{updated} applications accepted.')
    accept_applications.short_description = "Accept selected applications"
    
    def reject_applications(self, request, queryset):
        """Reject selected applications"""
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='rejected',
            responded_at=timezone.now()
        )
        self.message_user(request, f'{updated} applications rejected.')
    reject_applications.short_description = "Reject selected applications"
