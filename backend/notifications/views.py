from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notification, NotificationTemplate, NotificationPreference, NotificationLog
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer, NotificationUpdateSerializer,
    NotificationTemplateSerializer, NotificationPreferenceSerializer,
    NotificationPreferenceUpdateSerializer, NotificationLogSerializer
)

class NotificationViewSet(ModelViewSet):
    """ViewSet for Notification operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return NotificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        """Filter notifications by user"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        updated_count = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({
            'message': f'{updated_count} notifications marked as read.'
        })
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark specific notification as read"""
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        return Response({'message': 'Notification marked as read.'})

class NotificationPreferenceViewSet(ModelViewSet):
    """ViewSet for Notification Preference operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['update', 'partial_update']:
            return NotificationPreferenceUpdateSerializer
        return NotificationPreferenceSerializer
    
    def get_queryset(self):
        """Filter preferences by user"""
        return NotificationPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create notification preference"""
        serializer.save(user=self.request.user)

class NotificationTemplateViewSet(ModelViewSet):
    """ViewSet for Notification Template operations (Admin only)"""
    
    permission_classes = [permissions.IsAdminUser]
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer

class NotificationLogViewSet(ModelViewSet):
    """ViewSet for Notification Log operations (Admin only)"""
    
    permission_classes = [permissions.IsAdminUser]
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer

class NotificationStatsView(APIView):
    """View for notification statistics"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get notification statistics for user"""
        user_notifications = Notification.objects.filter(user=request.user)
        
        stats = {
            'total': user_notifications.count(),
            'unread': user_notifications.filter(is_read=False).count(),
            'read': user_notifications.filter(is_read=True).count(),
            'by_type': {},
            'by_priority': {}
        }
        
        # Count by notification type
        for notification_type, _ in Notification.NOTIFICATION_TYPE_CHOICES:
            count = user_notifications.filter(notification_type=notification_type).count()
            if count > 0:
                stats['by_type'][notification_type] = count
        
        # Count by priority
        for priority, _ in Notification.PRIORITY_CHOICES:
            count = user_notifications.filter(priority=priority).count()
            if count > 0:
                stats['by_priority'][priority] = count
        
        return Response(stats)

class NotificationTestView(APIView):
    """View for testing notifications (Admin only)"""
    
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        """Create a test notification"""
        user_id = request.data.get('user_id')
        notification_type = request.data.get('notification_type', 'system_message')
        title = request.data.get('title', 'Test Notification')
        message = request.data.get('message', 'This is a test notification.')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            priority='medium'
        )
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
