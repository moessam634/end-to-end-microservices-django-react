from django.contrib import admin
from .models import Notification, NotificationTemplate, NotificationPreference, NotificationLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'notification_type', 'title', 'priority',
        'is_read', 'is_sent', 'created_at'
    ]
    list_filter = ['notification_type', 'priority', 'is_read', 'is_sent', 'created_at']
    search_fields = ['user__email', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'notification_type', 'priority', 'title', 'message')
        }),
        ('Action & Delivery', {
            'fields': ('action_url', 'email_sent', 'sms_sent', 'push_sent')
        }),
        ('Related Objects', {
            'fields': ('gig', 'gig_application', 'musician_profile', 'venue_profile'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_sent', 'read_at')
        }),
        ('Scheduling', {
            'fields': ('scheduled_for',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_sent']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read"""
        updated = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_sent(self, request, queryset):
        """Mark selected notifications as sent"""
        updated = queryset.filter(is_sent=False).update(is_sent=True)
        self.message_user(request, f'{updated} notifications marked as sent.')
    mark_as_sent.short_description = "Mark selected notifications as sent"

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'template_type', 'notification_type',
        'is_active', 'is_default', 'created_at'
    ]
    list_filter = ['template_type', 'notification_type', 'is_active', 'is_default']
    search_fields = ['name', 'subject', 'body']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['template_type', 'notification_type']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template_type', 'notification_type')
        }),
        ('Content', {
            'fields': ('subject', 'body', 'available_variables')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_default')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'notification_type', 'is_enabled',
        'frequency', 'created_at'
    ]
    list_filter = ['notification_type', 'is_enabled', 'frequency', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user', 'notification_type']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'notification_type', 'is_enabled')
        }),
        ('Delivery Preferences', {
            'fields': ('delivery_methods', 'frequency')
        }),
        ('Timing Preferences', {
            'fields': ('quiet_hours_start', 'quiet_hours_end', 'timezone'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'notification', 'delivery_method', 'status',
        'attempted_at', 'delivered_at'
    ]
    list_filter = ['delivery_method', 'status', 'attempted_at']
    search_fields = ['notification__title', 'external_id', 'error_message']
    readonly_fields = ['attempted_at', 'delivered_at']
    ordering = ['-attempted_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('notification', 'delivery_method', 'status')
        }),
        ('External Service', {
            'fields': ('external_id', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('attempted_at', 'delivered_at')
        }),
    )
