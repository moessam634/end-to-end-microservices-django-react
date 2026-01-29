from django.contrib import admin
from .models import AIService, AIRecommendation, AITask

@admin.register(AIService)
class AIServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'content_type', 'status', 'ai_model', 
        'tokens_used', 'cost', 'created_at'
    ]
    list_filter = ['content_type', 'status', 'ai_model', 'created_at']
    search_fields = ['user__email', 'prompt', 'generated_content']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'content_type', 'status', 'ai_model')
        }),
        ('Content', {
            'fields': ('prompt', 'generated_content', 'input_data', 'metadata')
        }),
        ('Related Objects', {
            'fields': ('musician_profile', 'venue_profile', 'gig', 'gig_application'),
            'classes': ('collapse',)
        }),
        ('Usage & Cost', {
            'fields': ('tokens_used', 'cost'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'recommendation_type', 'title', 
        'confidence_score', 'is_viewed', 'is_accepted', 'created_at'
    ]
    list_filter = ['recommendation_type', 'is_viewed', 'is_accepted', 'created_at']
    search_fields = ['user__email', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-confidence_score', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'recommendation_type', 'title', 'description')
        }),
        ('Recommendation Details', {
            'fields': ('confidence_score', 'reasoning')
        }),
        ('Related Objects', {
            'fields': ('recommended_gig', 'recommended_musician', 'recommended_venue'),
            'classes': ('collapse',)
        }),
        ('User Interaction', {
            'fields': ('is_viewed', 'is_accepted', 'user_feedback')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AITask)
class AITaskAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'task_type', 'status', 'progress_percentage',
        'created_at', 'started_at', 'completed_at'
    ]
    list_filter = ['task_type', 'status', 'created_at']
    search_fields = ['user__email', 'celery_task_id', 'error_message']
    readonly_fields = [
        'created_at', 'started_at', 'completed_at', 'celery_task_id',
        'result_data', 'error_message'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'task_type', 'status', 'ai_service')
        }),
        ('Task Details', {
            'fields': ('celery_task_id', 'input_data', 'result_data', 'error_message')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'estimated_completion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
