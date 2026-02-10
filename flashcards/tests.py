from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Flashcard, StudySession


class FlashcardModelTests(TestCase):
    """Test cases for Flashcard model"""
    
    def setUp(self):
        """Set up test user and flashcard"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.flashcard = Flashcard.objects.create(
            user=self.user,
            front='What is Django?',
            back='A Python web framework',
            topic='Programming'
        )
    
    def test_flashcard_creation(self):
        """Test flashcard is created correctly"""
        self.assertEqual(self.flashcard.front, 'What is Django?')
        self.assertEqual(self.flashcard.back, 'A Python web framework')
        self.assertEqual(self.flashcard.topic, 'Programming')
        self.assertEqual(self.flashcard.user, self.user)
    
    def test_flashcard_str(self):
        """Test string representation of flashcard"""
        expected = f"Programming: {self.flashcard.front[:50]}"
        self.assertEqual(str(self.flashcard), expected)
    
    def test_mark_reviewed(self):
        """Test marking flashcard as reviewed"""
        self.assertEqual(self.flashcard.times_reviewed, 0)
        self.flashcard.mark_reviewed(is_correct=True)
        self.assertEqual(self.flashcard.times_reviewed, 1)
        self.assertEqual(self.flashcard.times_correct, 1)
    
    def test_success_rate(self):
        """Test success rate calculation"""
        self.flashcard.times_reviewed = 10
        self.flashcard.times_correct = 8
        self.assertEqual(self.flashcard.get_success_rate(), 80)


class FlashcardViewTests(TestCase):
    """Test cases for flashcard views"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.flashcard = Flashcard.objects.create(
            user=self.user,
            front='Test Question',
            back='Test Answer',
            topic='Test Topic'
        )
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('flashcards:dashboard'))
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_for_authenticated_user(self):
        """Test dashboard loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('flashcards:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/dashboard.html')
    
    def test_flashcard_list_view(self):
        """Test flashcard list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('flashcards:flashcard_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Question')
    
    def test_create_flashcard(self):
        """Test creating a new flashcard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('flashcards:flashcard_create'), {
            'front': 'New Question',
            'back': 'New Answer',
            'topic': 'New Topic'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Flashcard.objects.filter(front='New Question').exists())
    
    def test_edit_flashcard(self):
        """Test editing an existing flashcard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('flashcards:flashcard_edit', args=[self.flashcard.pk]),
            {
                'front': 'Updated Question',
                'back': 'Updated Answer',
                'topic': 'Updated Topic'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.flashcard.refresh_from_db()
        self.assertEqual(self.flashcard.front, 'Updated Question')
    
    def test_delete_flashcard(self):
        """Test deleting a flashcard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('flashcards:flashcard_delete', args=[self.flashcard.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Flashcard.objects.filter(pk=self.flashcard.pk).exists())
    
    def test_user_can_only_see_own_flashcards(self):
        """Test that users can only see their own flashcards"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_flashcard = Flashcard.objects.create(
            user=other_user,
            front='Other Question',
            back='Other Answer',
            topic='Other Topic'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('flashcards:flashcard_list'))
        
        self.assertContains(response, 'Test Question')
        self.assertNotContains(response, 'Other Question')


class StudySessionTests(TestCase):
    """Test cases for study sessions"""
    
    def setUp(self):
        """Set up test user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create some flashcards
        for i in range(5):
            Flashcard.objects.create(
                user=self.user,
                front=f'Question {i}',
                back=f'Answer {i}',
                topic='Test'
            )
    
    def test_study_mode_requires_login(self):
        """Test that study mode requires authentication"""
        response = self.client.get(reverse('flashcards:study_mode'))
        self.assertEqual(response.status_code, 302)
    
    def test_study_mode_loads(self):
        """Test that study mode loads correctly"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('flashcards:study_mode'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/study_mode.html')
