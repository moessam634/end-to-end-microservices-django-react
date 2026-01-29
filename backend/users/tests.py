from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
from datetime import date, datetime
from django.utils import timezone
from .models import User, MusicianProfile, VenueProfile

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'user_type': 'musician',
            'phone_number': '+1234567890',
            'bio': 'Test musician bio',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'website': 'https://test.com',
            'instagram': '@testuser',
            'facebook': 'testuser',
            'twitter': '@testuser',
        }
    
    def test_user_creation(self):
        """Test basic user creation"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.user_type, 'musician')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertEqual(user.bio, 'Test musician bio')
        self.assertEqual(user.city, 'Test City')
        self.assertEqual(user.state, 'Test State')
        self.assertEqual(user.country, 'Test Country')
        self.assertEqual(user.website, 'https://test.com')
        self.assertEqual(user.instagram, '@testuser')
        self.assertEqual(user.facebook, 'testuser')
        self.assertEqual(user.twitter, '@testuser')
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
    
    def test_user_str_representation(self):
        """Test string representation of user"""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.get_full_name()} ({user.email})"
        self.assertEqual(str(user), expected)
    
    def test_get_full_name(self):
        """Test get_full_name method"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'Test User')
        
        # Test with only first name
        user.first_name = 'Test'
        user.last_name = ''
        user.save()
        self.assertEqual(user.get_full_name(), 'testuser')
    
    def test_display_name_property(self):
        """Test display_name property"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.display_name, 'Test User')
        
        # Test with only username
        user.first_name = ''
        user.last_name = ''
        user.save()
        self.assertEqual(user.display_name, 'testuser')
    
    def test_user_type_properties(self):
        """Test user type properties"""
        # Test musician
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.is_musician)
        self.assertFalse(user.is_venue_owner)
        
        # Test venue owner
        user.user_type = 'venue'
        user.save()
        self.assertFalse(user.is_musician)
        self.assertTrue(user.is_venue_owner)
    
    def test_email_uniqueness(self):
        """Test that email must be unique"""
        User.objects.create_user(**self.user_data)
        
        # Try to create another user with same email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                username='anotheruser',
                password='testpass123'
            )
    
    def test_phone_number_validation(self):
        """Test phone number validation"""
        # Valid phone number
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.phone_number, '+1234567890')
        
        # Invalid phone number (should still save but with warning)
        user.phone_number = 'invalid'
        user.save()
        self.assertEqual(user.phone_number, 'invalid')
    
    def test_user_type_choices(self):
        """Test user type choices"""
        valid_types = ['musician', 'venue', 'admin']
        
        for user_type in valid_types:
            user = User.objects.create_user(
                email=f'test{user_type}@example.com',
                username=f'test{user_type}',
                password='testpass123',
                user_type=user_type
            )
            self.assertEqual(user.user_type, user_type)


class MusicianProfileModelTest(TestCase):
    """Test cases for the MusicianProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='musician@example.com',
            username='musician',
            password='testpass123',
            user_type='musician'
        )
        
        self.profile_data = {
            'user': self.user,
            'primary_instrument': 'Guitar',
            'instruments': ['Guitar', 'Piano', 'Vocals'],
            'genres': ['Rock', 'Pop', 'Jazz'],
            'experience_years': 5,
            'band_name': 'Test Band',
            'is_solo_artist': False,
            'band_size': 4,
            'setlist_examples': ['Song 1', 'Song 2', 'Song 3'],
            'original_music': True,
            'cover_music': True,
            'hourly_rate': Decimal('50.00'),
            'per_gig_rate': Decimal('200.00'),
            'availability_schedule': {'monday': 'available', 'tuesday': 'busy'},
            'travel_distance': 100,
            'portfolio_links': ['https://soundcloud.com/test', 'https://youtube.com/test'],
            'audio_samples': ['audio1.mp3', 'audio2.mp3'],
            'video_samples': ['video1.mp4', 'video2.mp4'],
            'ai_generated_bio': 'AI generated bio text',
            'ai_generated_setlist': ['AI Song 1', 'AI Song 2']
        }
    
    def test_musician_profile_creation(self):
        """Test musician profile creation"""
        profile = MusicianProfile.objects.create(**self.profile_data)
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.primary_instrument, 'Guitar')
        self.assertEqual(profile.instruments, ['Guitar', 'Piano', 'Vocals'])
        self.assertEqual(profile.genres, ['Rock', 'Pop', 'Jazz'])
        self.assertEqual(profile.experience_years, 5)
        self.assertEqual(profile.band_name, 'Test Band')
        self.assertFalse(profile.is_solo_artist)
        self.assertEqual(profile.band_size, 4)
        self.assertEqual(profile.setlist_examples, ['Song 1', 'Song 2', 'Song 3'])
        self.assertTrue(profile.original_music)
        self.assertTrue(profile.cover_music)
        self.assertEqual(profile.hourly_rate, Decimal('50.00'))
        self.assertEqual(profile.per_gig_rate, Decimal('200.00'))
        self.assertEqual(profile.availability_schedule, {'monday': 'available', 'tuesday': 'busy'})
        self.assertEqual(profile.travel_distance, 100)
        self.assertEqual(profile.portfolio_links, ['https://soundcloud.com/test', 'https://youtube.com/test'])
        self.assertEqual(profile.audio_samples, ['audio1.mp3', 'audio2.mp3'])
        self.assertEqual(profile.video_samples, ['video1.mp4', 'video2.mp4'])
        self.assertEqual(profile.ai_generated_bio, 'AI generated bio text')
        self.assertEqual(profile.ai_generated_setlist, ['AI Song 1', 'AI Song 2'])
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
    
    def test_musician_profile_str_representation(self):
        """Test string representation of musician profile"""
        profile = MusicianProfile.objects.create(**self.profile_data)
        expected = f"{self.user.get_full_name()} - Guitar"
        self.assertEqual(str(profile), expected)
    
    def test_one_to_one_relationship(self):
        """Test one-to-one relationship with User"""
        profile = MusicianProfile.objects.create(**self.profile_data)
        
        # Test accessing profile from user
        self.assertEqual(self.user.musician_profile, profile)
        
        # Test that only one profile can exist per user
        with self.assertRaises(IntegrityError):
            MusicianProfile.objects.create(
                user=self.user,
                primary_instrument='Piano'
            )


class VenueProfileModelTest(TestCase):
    """Test cases for the VenueProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='venue@example.com',
            username='venue',
            password='testpass123',
            user_type='venue'
        )
        
        self.profile_data = {
            'user': self.user,
            'venue_name': 'Test Venue',
            'venue_type': 'Bar',
            'capacity': 200,
            'address': '123 Test Street, Test City, TC 12345',
            'latitude': Decimal('40.7128'),
            'longitude': Decimal('-74.0060'),
            'has_stage': True,
            'has_sound_system': True,
            'has_lighting': True,
            'has_parking': True,
            'has_food': True,
            'has_alcohol': True,
            'preferred_genres': ['Rock', 'Pop', 'Jazz'],
            'preferred_instruments': ['Guitar', 'Drums', 'Bass'],
            'booking_lead_time': 14,
            'payment_terms': 'Net 30',
            'venue_photos': ['photo1.jpg', 'photo2.jpg'],
            'ai_generated_description': 'AI generated venue description',
            'ai_generated_marketing_copy': 'AI generated marketing copy'
        }
    
    def test_venue_profile_creation(self):
        """Test venue profile creation"""
        profile = VenueProfile.objects.create(**self.profile_data)
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.venue_name, 'Test Venue')
        self.assertEqual(profile.venue_type, 'Bar')
        self.assertEqual(profile.capacity, 200)
        self.assertEqual(profile.address, '123 Test Street, Test City, TC 12345')
        self.assertEqual(profile.latitude, Decimal('40.7128'))
        self.assertEqual(profile.longitude, Decimal('-74.0060'))
        self.assertTrue(profile.has_stage)
        self.assertTrue(profile.has_sound_system)
        self.assertTrue(profile.has_lighting)
        self.assertTrue(profile.has_parking)
        self.assertTrue(profile.has_food)
        self.assertTrue(profile.has_alcohol)
        self.assertEqual(profile.preferred_genres, ['Rock', 'Pop', 'Jazz'])
        self.assertEqual(profile.preferred_instruments, ['Guitar', 'Drums', 'Bass'])
        self.assertEqual(profile.booking_lead_time, 14)
        self.assertEqual(profile.payment_terms, 'Net 30')
        self.assertEqual(profile.venue_photos, ['photo1.jpg', 'photo2.jpg'])
        self.assertEqual(profile.ai_generated_description, 'AI generated venue description')
        self.assertEqual(profile.ai_generated_marketing_copy, 'AI generated marketing copy')
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
    
    def test_venue_profile_str_representation(self):
        """Test string representation of venue profile"""
        profile = VenueProfile.objects.create(**self.profile_data)
        self.assertEqual(str(profile), 'Test Venue')
    
    def test_one_to_one_relationship(self):
        """Test one-to-one relationship with User"""
        profile = VenueProfile.objects.create(**self.profile_data)
        
        # Test accessing profile from user
        self.assertEqual(self.user.venue_profile, profile)
        
        # Test that only one profile can exist per user
        with self.assertRaises(IntegrityError):
            VenueProfile.objects.create(
                user=self.user,
                venue_name='Another Venue',
                venue_type='Club',
                capacity=100,
                address='456 Another Street'
            )


class UserManagerTest(TestCase):
    """Test cases for User manager methods"""
    
    def test_create_user(self):
        """Test create_user method"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test create_superuser method"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        
        self.assertTrue(user.check_password('adminpass123'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
