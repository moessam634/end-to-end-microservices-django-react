from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .models import AIService, AIRecommendation, AITask
from .serializers import (
    AIServiceSerializer, AIServiceCreateSerializer, AIRecommendationSerializer,
    AIRecommendationUpdateSerializer, AITaskSerializer, AITaskCreateSerializer
)
from users.models import MusicianProfile, VenueProfile
from gigs.models import Gig, GigApplication

class AIServiceViewSet(ModelViewSet):
    """ViewSet for AI Service operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return AIServiceCreateSerializer
        return AIServiceSerializer
    
    def get_queryset(self):
        """Filter AI services by user"""
        return AIService.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create AI service request"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_content(self, request, pk=None):
        """Generate AI content for a service"""
        ai_service = self.get_object()
        
        if ai_service.status != 'pending':
            return Response(
                {'error': 'AI service is not in pending status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status to processing
        ai_service.status = 'processing'
        ai_service.save()
        
        # TODO: Trigger Celery task for AI content generation
        # For now, we'll simulate the process
        
        return Response({
            'message': 'AI content generation started.',
            'task_id': f'task_{ai_service.id}'
        })

class AIRecommendationViewSet(ModelViewSet):
    """ViewSet for AI Recommendation operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['update', 'partial_update']:
            return AIRecommendationUpdateSerializer
        return AIRecommendationSerializer
    
    def get_queryset(self):
        """Filter recommendations by user"""
        return AIRecommendation.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_viewed(self, request, pk=None):
        """Mark recommendation as viewed"""
        recommendation = self.get_object()
        recommendation.is_viewed = True
        recommendation.save()
        
        return Response({'message': 'Recommendation marked as viewed.'})
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a recommendation"""
        recommendation = self.get_object()
        recommendation.is_accepted = True
        recommendation.is_viewed = True
        recommendation.save()
        
        return Response({'message': 'Recommendation accepted.'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a recommendation"""
        recommendation = self.get_object()
        recommendation.is_accepted = False
        recommendation.is_viewed = True
        recommendation.save()
        
        return Response({'message': 'Recommendation rejected.'})

class AITaskViewSet(ModelViewSet):
    """ViewSet for AI Task operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return AITaskCreateSerializer
        return AITaskSerializer
    
    def get_queryset(self):
        """Filter tasks by user"""
        return AITask.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create AI task"""
        serializer.save(user=self.request.user)

class AIContentGenerationView(APIView):
    """View for generating AI content"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Generate AI content based on type"""
        content_type = request.data.get('content_type')
        input_data = request.data.get('input_data', {})
        
        if not content_type:
            return Response(
                {'error': 'content_type is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate content type
        valid_types = [choice[0] for choice in AIService.CONTENT_TYPE_CHOICES]
        if content_type not in valid_types:
            return Response(
                {'error': f'Invalid content_type. Must be one of: {valid_types}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create AI service request
        ai_service_data = {
            'content_type': content_type,
            'input_data': input_data,
            'prompt': self._generate_prompt(content_type, input_data)
        }
        
        # Add related objects based on content type
        if content_type == 'musician_bio':
            musician_id = input_data.get('musician_profile_id')
            if musician_id:
                ai_service_data['musician_profile'] = musician_id
        
        elif content_type == 'venue_description':
            venue_id = input_data.get('venue_profile_id')
            if venue_id:
                ai_service_data['venue_profile'] = venue_id
        
        elif content_type in ['gig_description', 'marketing_copy']:
            gig_id = input_data.get('gig_id')
            if gig_id:
                ai_service_data['gig'] = gig_id
        
        elif content_type in ['cover_letter', 'proposal']:
            application_id = input_data.get('gig_application_id')
            if application_id:
                ai_service_data['gig_application'] = application_id
        
        serializer = AIServiceCreateSerializer(
            data=ai_service_data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            ai_service = serializer.save(user=request.user)
            
            # TODO: Trigger Celery task for actual AI generation
            # For now, return the created service
            
            return Response(
                AIServiceSerializer(ai_service).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _generate_prompt(self, content_type, input_data):
        """Generate appropriate prompt based on content type"""
        prompts = {
            'musician_bio': f"Generate a professional musician bio for {input_data.get('name', 'musician')}",
            'venue_description': f"Generate a venue description for {input_data.get('venue_name', 'venue')}",
            'gig_description': f"Generate a gig description for {input_data.get('title', 'gig')}",
            'setlist': f"Generate a setlist for {input_data.get('genre', 'music')} performance",
            'cover_letter': f"Generate a cover letter for gig application",
            'marketing_copy': f"Generate marketing copy for {input_data.get('title', 'event')}",
            'proposal': f"Generate a gig proposal"
        }
        
        return prompts.get(content_type, f"Generate {content_type}")

class AIGigMatchingView(APIView):
    """View for AI-powered gig matching"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Find matching gigs for musician"""
        if not request.user.is_musician:
            return Response(
                {'error': 'Only musicians can use gig matching.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            musician_profile = MusicianProfile.objects.get(user=request.user)
        except MusicianProfile.DoesNotExist:
            return Response(
                {'error': 'Musician profile not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get matching gigs based on musician profile
        matching_gigs = self._find_matching_gigs(musician_profile)
        
        # Create recommendations
        recommendations = []
        for gig in matching_gigs:
            recommendation = AIRecommendation.objects.create(
                user=request.user,
                recommendation_type='gig_match',
                title=f"Perfect Match: {gig.title}",
                description=f"This gig at {gig.venue.venue_name} matches your profile perfectly!",
                confidence_score=self._calculate_match_score(musician_profile, gig),
                reasoning=self._generate_match_reasoning(musician_profile, gig),
                recommended_gig=gig
            )
            recommendations.append(recommendation)
        
        serializer = AIRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
    
    def _find_matching_gigs(self, musician_profile):
        """Find gigs that match musician profile"""
        from django.db.models import Q
        
        # Basic matching criteria
        queryset = Gig.objects.filter(status='open')
        
        # Match genres
        if musician_profile.genres:
            queryset = queryset.filter(genres__overlap=musician_profile.genres)
        
        # Match instruments
        if musician_profile.instruments:
            queryset = queryset.filter(instruments_needed__overlap=musician_profile.instruments)
        
        # Match experience level
        queryset = queryset.filter(experience_level__lte=musician_profile.experience_years)
        
        # Match location (within travel distance)
        if musician_profile.user.city:
            # TODO: Implement location-based matching
            pass
        
        return queryset[:10]  # Return top 10 matches
    
    def _calculate_match_score(self, musician_profile, gig):
        """Calculate match score between musician and gig"""
        score = 0.0
        
        # Genre match
        if musician_profile.genres and gig.genres:
            genre_matches = len(set(musician_profile.genres) & set(gig.genres))
            score += (genre_matches / len(gig.genres)) * 0.4
        
        # Instrument match
        if musician_profile.instruments and gig.instruments_needed:
            instrument_matches = len(set(musician_profile.instruments) & set(gig.instruments_needed))
            score += (instrument_matches / len(gig.instruments_needed)) * 0.3
        
        # Experience match
        if musician_profile.experience_years >= 5:
            score += 0.2
        elif musician_profile.experience_years >= 2:
            score += 0.1
        
        # Original music preference
        if musician_profile.original_music == gig.original_music_required:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_match_reasoning(self, musician_profile, gig):
        """Generate reasoning for match"""
        reasons = []
        
        if musician_profile.genres and gig.genres:
            common_genres = set(musician_profile.genres) & set(gig.genres)
            if common_genres:
                reasons.append(f"Genre match: {', '.join(common_genres)}")
        
        if musician_profile.instruments and gig.instruments_needed:
            common_instruments = set(musician_profile.instruments) & set(gig.instruments_needed)
            if common_instruments:
                reasons.append(f"Instrument match: {', '.join(common_instruments)}")
        
        if musician_profile.experience_years >= gig.band_size_min:
            reasons.append(f"Experience level suitable ({musician_profile.experience_years} years)")
        
        return "; ".join(reasons) if reasons else "Good general match"
