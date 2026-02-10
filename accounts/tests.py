from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsViewTests(TestCase):
    """Test cases for accounts views"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_signup_page_loads(self):
        """Test that signup page loads successfully"""
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_user_can_login(self):
        """Test that user can login with correct credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
    
    def test_user_can_signup(self):
        """Test that new user can sign up"""
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123!',
            'password2': 'newpass123!'
        })
        # Should redirect after successful signup
        self.assertEqual(response.status_code, 302)
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_profile_requires_login(self):
        """Test that profile page requires authentication"""
        response = self.client.get(reverse('accounts:profile'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_profile_page_for_authenticated_user(self):
        """Test that authenticated user can access profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
