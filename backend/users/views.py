from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User, MusicianProfile, VenueProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer, MusicianProfileSerializer,
    VenueProfileSerializer, UserProfileSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create profile based on user type
        if user.user_type == 'musician':
            MusicianProfile.objects.create(
                user=user,
                primary_instrument='Guitar',  # Default value
                experience_years=0
            )
        elif user.user_type == 'venue':
            VenueProfile.objects.create(
                user=user,
                venue_name=f"{user.first_name}'s Venue",  # Default value
                venue_type='Bar',  # Default value
                capacity=100,  # Default value
                address='',  # Will be filled later
                booking_lead_time=7
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token)
            })
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class MusicianProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MusicianProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(MusicianProfile, user=self.request.user)

class MusicianProfileUpdateView(generics.UpdateAPIView):
    serializer_class = MusicianProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(MusicianProfile, user=self.request.user)

class VenueProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VenueProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(VenueProfile, user=self.request.user)

class VenueProfileUpdateView(generics.UpdateAPIView):
    serializer_class = VenueProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(VenueProfile, user=self.request.user)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
