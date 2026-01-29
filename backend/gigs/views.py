from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Gig, GigApplication
from .serializers import (
    GigSerializer, GigCreateSerializer, GigApplicationSerializer,
    GigApplicationCreateSerializer, GigApplicationUpdateSerializer
)
from users.models import MusicianProfile, VenueProfile

class GigViewSet(ModelViewSet):
    """ViewSet for Gig CRUD operations"""
    
    queryset = Gig.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'genres', 'experience_level', 'payment_type']
    search_fields = ['title', 'description', 'venue__venue_name']
    ordering_fields = ['event_date', 'created_at', 'payment_amount']
    ordering = ['-event_date']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return GigCreateSerializer
        return GigSerializer
    
    def get_queryset(self):
        """Filter gigs based on user type and permissions"""
        queryset = super().get_queryset()
        
        # Filter by user type
        if self.request.user.is_musician:
            # Musicians see all open gigs and their applications
            queryset = queryset.filter(
                Q(status='open') | 
                Q(applications__musician__user=self.request.user)
            ).distinct()
        elif self.request.user.is_venue_owner:
            # Venue owners see their own gigs
            queryset = queryset.filter(venue__user=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create gig and set venue"""
        venue_id = serializer.validated_data['venue_id']
        venue = get_object_or_404(VenueProfile, id=venue_id, user=self.request.user)
        serializer.save(venue=venue)
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Apply to a gig"""
        gig = self.get_object()
        
        if not request.user.is_musician:
            return Response(
                {'error': 'Only musicians can apply to gigs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not gig.is_open_for_applications:
            return Response(
                {'error': 'This gig is not accepting applications.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get musician profile
        try:
            musician_profile = MusicianProfile.objects.get(user=request.user)
        except MusicianProfile.DoesNotExist:
            return Response(
                {'error': 'Musician profile not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already applied
        if GigApplication.objects.filter(gig=gig, musician=musician_profile).exists():
            return Response(
                {'error': 'You have already applied to this gig.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create application
        application_data = request.data.copy()
        application_data['gig_id'] = gig.id
        application_data['musician_id'] = musician_profile.id
        
        serializer = GigApplicationCreateSerializer(
            data=application_data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            application = serializer.save(gig=gig, musician=musician_profile)
            return Response(
                GigApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get applications for a gig"""
        gig = self.get_object()
        
        # Only venue owner can see applications
        if gig.venue.user != request.user:
            return Response(
                {'error': 'You can only view applications for your own gigs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        applications = gig.applications.all()
        serializer = GigApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a gig (stop accepting applications)"""
        gig = self.get_object()
        
        if gig.venue.user != request.user:
            return Response(
                {'error': 'You can only close your own gigs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        gig.status = 'pending'
        gig.save()
        
        return Response({'message': 'Gig closed successfully.'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a gig"""
        gig = self.get_object()
        
        if gig.venue.user != request.user:
            return Response(
                {'error': 'You can only cancel your own gigs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        gig.status = 'cancelled'
        gig.save()
        
        return Response({'message': 'Gig cancelled successfully.'})

class GigApplicationViewSet(ModelViewSet):
    """ViewSet for Gig Application operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'gig__status']
    ordering_fields = ['applied_at', 'updated_at']
    ordering = ['-applied_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return GigApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GigApplicationUpdateSerializer
        return GigApplicationSerializer
    
    def get_queryset(self):
        """Filter applications based on user type"""
        if self.request.user.is_musician:
            # Musicians see their own applications
            return GigApplication.objects.filter(
                musician__user=self.request.user
            )
        elif self.request.user.is_venue_owner:
            # Venue owners see applications to their gigs
            return GigApplication.objects.filter(
                gig__venue__user=self.request.user
            )
        return GigApplication.objects.none()
    
    def perform_create(self, serializer):
        """Create application"""
        gig_id = serializer.validated_data['gig_id']
        musician_id = serializer.validated_data['musician_id']
        
        gig = get_object_or_404(Gig, id=gig_id)
        musician = get_object_or_404(MusicianProfile, id=musician_id)
        
        serializer.save(gig=gig, musician=musician)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a gig application"""
        application = self.get_object()
        
        # Only venue owner can accept applications
        if application.gig.venue.user != request.user:
            return Response(
                {'error': 'You can only accept applications for your own gigs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if application.status != 'pending':
            return Response(
                {'error': 'Application is not pending.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'accepted'
        application.responded_at = timezone.now()
        application.save()
        
        # Update gig status to confirmed
        application.gig.status = 'confirmed'
        application.gig.save()
        
        return Response({'message': 'Application accepted successfully.'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a gig application"""
        application = self.get_object()
        
        # Only venue owner can reject applications
        if application.gig.venue.user != request.user:
            return Response(
                {'error': 'You can only reject applications for your own gigs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if application.status != 'pending':
            return Response(
                {'error': 'Application is not pending.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'rejected'
        application.responded_at = timezone.now()
        application.save()
        
        return Response({'message': 'Application rejected successfully.'})
    
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        """Withdraw a gig application"""
        application = self.get_object()
        
        # Only musician can withdraw their own application
        if application.musician.user != request.user:
            return Response(
                {'error': 'You can only withdraw your own applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if application.status != 'pending':
            return Response(
                {'error': 'Application is not pending.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'withdrawn'
        application.save()
        
        return Response({'message': 'Application withdrawn successfully.'})

class GigSearchView(APIView):
    """Advanced gig search with filters"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Search gigs with advanced filters"""
        queryset = Gig.objects.filter(status='open')
        
        # Location filter
        city = request.query_params.get('city')
        state = request.query_params.get('state')
        if city:
            queryset = queryset.filter(venue__user__city__icontains=city)
        if state:
            queryset = queryset.filter(venue__user__state__icontains=state)
        
        # Date filters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(event_date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(event_date__date__lte=date_to)
        
        # Payment filter
        min_payment = request.query_params.get('min_payment')
        max_payment = request.query_params.get('max_payment')
        if min_payment:
            queryset = queryset.filter(payment_amount__gte=min_payment)
        if max_payment:
            queryset = queryset.filter(payment_amount__lte=max_payment)
        
        # Genre filter
        genres = request.query_params.getlist('genres')
        if genres:
            queryset = queryset.filter(genres__overlap=genres)
        
        # Experience level filter
        experience_level = request.query_params.get('experience_level')
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
        
        # Sort by
        sort_by = request.query_params.get('sort_by', 'event_date')
        if sort_by == 'payment':
            queryset = queryset.order_by('-payment_amount')
        elif sort_by == 'date':
            queryset = queryset.order_by('event_date')
        elif sort_by == 'created':
            queryset = queryset.order_by('-created_at')
        
        # Pagination
        page_size = int(request.query_params.get('page_size', 20))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        gigs = queryset[start:end]
        serializer = GigSerializer(gigs, many=True)
        
        return Response({
            'results': serializer.data,
            'count': queryset.count(),
            'page': page,
            'page_size': page_size
        })

class MyGigsView(APIView):
    """Get user's gigs (created or applied to)"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user's gigs"""
        if request.user.is_venue_owner:
            # Venue owner's created gigs
            gigs = Gig.objects.filter(venue__user=request.user)
            serializer = GigSerializer(gigs, many=True)
            return Response({
                'created_gigs': serializer.data
            })
        
        elif request.user.is_musician:
            # Musician's applications
            applications = GigApplication.objects.filter(
                musician__user=request.user
            )
            application_serializer = GigApplicationSerializer(applications, many=True)
            
            # Gigs they've applied to
            applied_gigs = Gig.objects.filter(
                applications__musician__user=request.user
            ).distinct()
            gig_serializer = GigSerializer(applied_gigs, many=True)
            
            return Response({
                'applications': application_serializer.data,
                'applied_gigs': gig_serializer.data
            })
        
        return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)
