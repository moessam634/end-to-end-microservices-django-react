from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
from users.models import User, MusicianProfile, VenueProfile
from .models import Gig, GigApplication


class GigModelTest(TestCase):
    """Test cases for the Gig model"""
    
    def setUp(self):
        """Set up test data"""
        # Create venue user and profile
        self.venue_user = User.objects.create_user(
            email='venue@example.com',
            username='venue',
            password='testpass123',
            user_type='venue'
        )
        
        self.venue_profile = VenueProfile.objects.create(
            user=self.venue_user,
            venue_name='Test Venue',
            venue_type='Bar',
            capacity=200,
            address='123 Test Street, Test City, TC 12345'
        )
        
        # Create musician user and profile
        self.musician_user = User.objects.create_user(
            email='musician@example.com',
            username='musician',
            password='testpass123',
            user_type='musician'
        )
        
        self.musician_profile = MusicianProfile.objects.create(
            user=self.musician_user,
            primary_instrument='Guitar',
            instruments=['Guitar', 'Piano'],
            genres=['Rock', 'Pop']
        )
        
        # Future event date
        self.future_date = timezone.now() + timedelta(days=30)
        
        self.gig_data = {
            'title': 'Friday Night Live Music',
            'description': 'Looking for a rock band to perform on Friday night',
            'venue': self.venue_profile,
            'event_date': self.future_date,
            'duration_hours': 3,
            'setup_time': 45,
            'genres': ['Rock', 'Pop'],
            'instruments_needed': ['Guitar', 'Drums', 'Bass', 'Vocals'],
            'band_size_min': 3,
            'band_size_max': 5,
            'payment_amount': Decimal('500.00'),
            'payment_type': 'per_gig',
            'experience_level': 'professional',
            'original_music_required': False,
            'cover_music_required': True,
            'sound_system_provided': True,
            'lighting_provided': True,
            'backline_provided': False,
            'special_requirements': 'Must have own transportation',
            'contact_person': 'John Doe',
            'contact_phone': '+1234567890',
            'contact_email': 'john@testvenue.com',
            'status': 'open',
            'is_featured': False,
            'is_urgent': False,
            'ai_generated_description': 'AI generated gig description',
            'ai_generated_marketing_copy': 'AI generated marketing copy',
            'deadline': self.future_date - timedelta(days=7)
        }
    
    def test_gig_creation(self):
        """Test basic gig creation"""
        gig = Gig.objects.create(**self.gig_data)
        
        self.assertEqual(gig.title, 'Friday Night Live Music')
        self.assertEqual(gig.description, 'Looking for a rock band to perform on Friday night')
        self.assertEqual(gig.venue, self.venue_profile)
        self.assertEqual(gig.event_date, self.future_date)
        self.assertEqual(gig.duration_hours, 3)
        self.assertEqual(gig.setup_time, 45)
        self.assertEqual(gig.genres, ['Rock', 'Pop'])
        self.assertEqual(gig.instruments_needed, ['Guitar', 'Drums', 'Bass', 'Vocals'])
        self.assertEqual(gig.band_size_min, 3)
        self.assertEqual(gig.band_size_max, 5)
        self.assertEqual(gig.payment_amount, Decimal('500.00'))
        self.assertEqual(gig.payment_type, 'per_gig')
        self.assertEqual(gig.experience_level, 'professional')
        self.assertFalse(gig.original_music_required)
        self.assertTrue(gig.cover_music_required)
        self.assertTrue(gig.sound_system_provided)
        self.assertTrue(gig.lighting_provided)
        self.assertFalse(gig.backline_provided)
        self.assertEqual(gig.special_requirements, 'Must have own transportation')
        self.assertEqual(gig.contact_person, 'John Doe')
        self.assertEqual(gig.contact_phone, '+1234567890')
        self.assertEqual(gig.contact_email, 'john@testvenue.com')
        self.assertEqual(gig.status, 'open')
        self.assertFalse(gig.is_featured)
        self.assertFalse(gig.is_urgent)
        self.assertEqual(gig.ai_generated_description, 'AI generated gig description')
        self.assertEqual(gig.ai_generated_marketing_copy, 'AI generated marketing copy')
        self.assertIsNotNone(gig.created_at)
        self.assertIsNotNone(gig.updated_at)
    
    def test_gig_str_representation(self):
        """Test string representation of gig"""
        gig = Gig.objects.create(**self.gig_data)
        expected = f"{gig.title} at {gig.venue.venue_name} - {gig.event_date.strftime('%B %d, %Y')}"
        self.assertEqual(str(gig), expected)
    
    def test_is_open_for_applications_property(self):
        """Test is_open_for_applications property"""
        # Test open gig with future deadline
        gig = Gig.objects.create(**self.gig_data)
        self.assertTrue(gig.is_open_for_applications)
        
        # Test closed gig
        gig.status = 'confirmed'
        gig.save()
        self.assertFalse(gig.is_open_for_applications)
        
        # Test gig with past deadline
        gig.status = 'open'
        gig.deadline = timezone.now() - timedelta(days=1)
        gig.save()
        self.assertFalse(gig.is_open_for_applications)
        
        # Test gig without deadline
        gig.deadline = None
        gig.save()
        self.assertTrue(gig.is_open_for_applications)
    
    def test_days_until_event_property(self):
        """Test days_until_event property"""
        gig = Gig.objects.create(**self.gig_data)
        expected_days = (gig.event_date - timezone.now()).days
        self.assertEqual(gig.days_until_event, expected_days)
    
    def test_gig_status_choices(self):
        """Test gig status choices"""
        valid_statuses = ['open', 'pending', 'confirmed', 'cancelled', 'completed']
        
        for status in valid_statuses:
            gig = Gig.objects.create(**self.gig_data)
            gig.status = status
            gig.save()
            self.assertEqual(gig.status, status)
    
    def test_payment_type_choices(self):
        """Test payment type choices"""
        valid_payment_types = ['per_gig', 'per_hour', 'negotiable']
        
        for payment_type in valid_payment_types:
            gig = Gig.objects.create(**self.gig_data)
            gig.payment_type = payment_type
            gig.save()
            self.assertEqual(gig.payment_type, payment_type)
    
    def test_experience_level_choices(self):
        """Test experience level choices"""
        valid_levels = ['beginner', 'intermediate', 'professional']
        
        for level in valid_levels:
            gig = Gig.objects.create(**self.gig_data)
            gig.experience_level = level
            gig.save()
            self.assertEqual(gig.experience_level, level)
    
    def test_gig_ordering(self):
        """Test gig ordering by event_date and created_at"""
        # Create gigs with different dates
        past_gig = Gig.objects.create(
            **self.gig_data,
            title='Past Gig',
            event_date=timezone.now() - timedelta(days=10)
        )
        
        future_gig = Gig.objects.create(
            **self.gig_data,
            title='Future Gig',
            event_date=timezone.now() + timedelta(days=10)
        )
        
        recent_gig = Gig.objects.create(
            **self.gig_data,
            title='Recent Gig',
            event_date=timezone.now() + timedelta(days=5)
        )
        
        # Test ordering (should be by event_date descending, then created_at descending)
        gigs = list(Gig.objects.all())
        self.assertEqual(gigs[0], future_gig)  # Most future date
        self.assertEqual(gigs[1], recent_gig)  # Second most future date
        self.assertEqual(gigs[2], past_gig)    # Past date


class GigApplicationModelTest(TestCase):
    """Test cases for the GigApplication model"""
    
    def setUp(self):
        """Set up test data"""
        # Create venue user and profile
        self.venue_user = User.objects.create_user(
            email='venue@example.com',
            username='venue',
            password='testpass123',
            user_type='venue'
        )
        
        self.venue_profile = VenueProfile.objects.create(
            user=self.venue_user,
            venue_name='Test Venue',
            venue_type='Bar',
            capacity=200,
            address='123 Test Street, Test City, TC 12345'
        )
        
        # Create musician user and profile
        self.musician_user = User.objects.create_user(
            email='musician@example.com',
            username='musician',
            password='testpass123',
            user_type='musician'
        )
        
        self.musician_profile = MusicianProfile.objects.create(
            user=self.musician_user,
            primary_instrument='Guitar',
            instruments=['Guitar', 'Piano'],
            genres=['Rock', 'Pop']
        )
        
        # Create gig
        self.gig = Gig.objects.create(
            title='Friday Night Live Music',
            description='Looking for a rock band',
            venue=self.venue_profile,
            event_date=timezone.now() + timedelta(days=30),
            payment_amount=Decimal('500.00'),
            payment_type='per_gig'
        )
        
        self.application_data = {
            'gig': self.gig,
            'musician': self.musician_profile,
            'cover_letter': 'I am very interested in this gig opportunity...',
            'proposed_setlist': ['Song 1', 'Song 2', 'Song 3'],
            'proposed_duration': 3,
            'proposed_rate': Decimal('450.00'),
            'portfolio_links': ['https://soundcloud.com/test'],
            'audio_samples': ['audio1.mp3'],
            'video_samples': ['video1.mp4'],
            'status': 'pending',
            'venue_notes': 'Great musician!',
            'musician_notes': 'Looking forward to this gig',
            'ai_generated_cover_letter': 'AI generated cover letter',
            'ai_generated_setlist': ['AI Song 1', 'AI Song 2']
        }
    
    def test_gig_application_creation(self):
        """Test basic gig application creation"""
        application = GigApplication.objects.create(**self.application_data)
        
        self.assertEqual(application.gig, self.gig)
        self.assertEqual(application.musician, self.musician_profile)
        self.assertEqual(application.cover_letter, 'I am very interested in this gig opportunity...')
        self.assertEqual(application.proposed_setlist, ['Song 1', 'Song 2', 'Song 3'])
        self.assertEqual(application.proposed_duration, 3)
        self.assertEqual(application.proposed_rate, Decimal('450.00'))
        self.assertEqual(application.portfolio_links, ['https://soundcloud.com/test'])
        self.assertEqual(application.audio_samples, ['audio1.mp3'])
        self.assertEqual(application.video_samples, ['video1.mp4'])
        self.assertEqual(application.status, 'pending')
        self.assertEqual(application.venue_notes, 'Great musician!')
        self.assertEqual(application.musician_notes, 'Looking forward to this gig')
        self.assertEqual(application.ai_generated_cover_letter, 'AI generated cover letter')
        self.assertEqual(application.ai_generated_setlist, ['AI Song 1', 'AI Song 2'])
        self.assertIsNotNone(application.applied_at)
        self.assertIsNotNone(application.updated_at)
        self.assertIsNone(application.responded_at)
    
    def test_gig_application_str_representation(self):
        """Test string representation of gig application"""
        application = GigApplication.objects.create(**self.application_data)
        expected = f"{self.musician_profile.user.get_full_name()} - {self.gig.title}"
        self.assertEqual(str(application), expected)
    
    def test_unique_together_constraint(self):
        """Test that a musician can only apply once per gig"""
        GigApplication.objects.create(**self.application_data)
        
        # Try to create another application for the same gig and musician
        with self.assertRaises(IntegrityError):
            GigApplication.objects.create(
                gig=self.gig,
                musician=self.musician_profile,
                cover_letter='Another application'
            )
    
    def test_application_status_properties(self):
        """Test application status properties"""
        application = GigApplication.objects.create(**self.application_data)
        
        # Test pending status
        self.assertTrue(application.is_pending)
        self.assertFalse(application.is_accepted)
        self.assertFalse(application.is_rejected)
        
        # Test accepted status
        application.status = 'accepted'
        application.save()
        self.assertFalse(application.is_pending)
        self.assertTrue(application.is_accepted)
        self.assertFalse(application.is_rejected)
        
        # Test rejected status
        application.status = 'rejected'
        application.save()
        self.assertFalse(application.is_pending)
        self.assertFalse(application.is_accepted)
        self.assertTrue(application.is_rejected)
    
    def test_application_status_choices(self):
        """Test application status choices"""
        valid_statuses = ['pending', 'accepted', 'rejected', 'withdrawn']
        
        for status in valid_statuses:
            application = GigApplication.objects.create(**self.application_data)
            application.status = status
            application.save()
            self.assertEqual(application.status, status)
    
    def test_application_ordering(self):
        """Test application ordering by applied_at"""
        # Create applications at different times
        first_application = GigApplication.objects.create(**self.application_data)
        
        # Create another musician and application
        another_musician = MusicianProfile.objects.create(
            user=User.objects.create_user(
                email='another@example.com',
                username='another',
                password='testpass123',
                user_type='musician'
            ),
            primary_instrument='Piano'
        )
        
        second_application = GigApplication.objects.create(
            gig=self.gig,
            musician=another_musician,
            cover_letter='Another application'
        )
        
        # Test ordering (should be by applied_at descending)
        applications = list(GigApplication.objects.all())
        self.assertEqual(applications[0], second_application)  # Most recent
        self.assertEqual(applications[1], first_application)   # Older


class GigApplicationRelationshipTest(TestCase):
    """Test cases for relationships between Gig and GigApplication"""
    
    def setUp(self):
        """Set up test data"""
        # Create venue
        self.venue_user = User.objects.create_user(
            email='venue@example.com',
            username='venue',
            password='testpass123',
            user_type='venue'
        )
        
        self.venue_profile = VenueProfile.objects.create(
            user=self.venue_user,
            venue_name='Test Venue',
            venue_type='Bar',
            capacity=200,
            address='123 Test Street'
        )
        
        # Create musicians
        self.musician1 = MusicianProfile.objects.create(
            user=User.objects.create_user(
                email='musician1@example.com',
                username='musician1',
                password='testpass123',
                user_type='musician'
            ),
            primary_instrument='Guitar'
        )
        
        self.musician2 = MusicianProfile.objects.create(
            user=User.objects.create_user(
                email='musician2@example.com',
                username='musician2',
                password='testpass123',
                user_type='musician'
            ),
            primary_instrument='Piano'
        )
        
        # Create gig
        self.gig = Gig.objects.create(
            title='Test Gig',
            description='Test description',
            venue=self.venue_profile,
            event_date=timezone.now() + timedelta(days=30),
            payment_amount=Decimal('500.00'),
            payment_type='per_gig'
        )
    
    def test_gig_applications_relationship(self):
        """Test accessing applications from gig"""
        # Create applications
        app1 = GigApplication.objects.create(
            gig=self.gig,
            musician=self.musician1,
            cover_letter='Application 1'
        )
        
        app2 = GigApplication.objects.create(
            gig=self.gig,
            musician=self.musician2,
            cover_letter='Application 2'
        )
        
        # Test accessing applications from gig
        applications = self.gig.applications.all()
        self.assertEqual(len(applications), 2)
        self.assertIn(app1, applications)
        self.assertIn(app2, applications)
    
    def test_musician_gig_applications_relationship(self):
        """Test accessing gig applications from musician"""
        # Create applications
        app1 = GigApplication.objects.create(
            gig=self.gig,
            musician=self.musician1,
            cover_letter='Application 1'
        )
        
        # Create another gig and application
        another_gig = Gig.objects.create(
            title='Another Gig',
            description='Another description',
            venue=self.venue_profile,
            event_date=timezone.now() + timedelta(days=35),
            payment_amount=Decimal('300.00'),
            payment_type='per_gig'
        )
        
        app2 = GigApplication.objects.create(
            gig=another_gig,
            musician=self.musician1,
            cover_letter='Application 2'
        )
        
        # Test accessing applications from musician
        applications = self.musician1.gig_applications.all()
        self.assertEqual(len(applications), 2)
        self.assertIn(app1, applications)
        self.assertIn(app2, applications)
