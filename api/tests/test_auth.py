from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class JWTAuthenticationTestCase(TestCase):
    """Test case for JWT authentication endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

        # Create test user
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='test@example.com'
        )

    def test_obtain_jwt_token_success(self):
        """Test obtaining JWT token with valid credentials"""
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.token_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])

    def test_obtain_jwt_token_invalid_credentials(self):
        """Test obtaining JWT token with invalid credentials"""
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_jwt_token_missing_username(self):
        """Test obtaining JWT token without username"""
        data = {
            'password': self.password
        }
        response = self.client.post(self.token_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_jwt_token_missing_password(self):
        """Test obtaining JWT token without password"""
        data = {
            'username': self.username
        }
        response = self.client.post(self.token_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_jwt_token_success(self):
        """Test refreshing JWT token with valid refresh token"""
        # First, obtain tokens
        data = {
            'username': self.username,
            'password': self.password
        }
        token_response = self.client.post(self.token_url, data, format='json')
        refresh_token = token_response.data['refresh']

        # Now refresh the token
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIsNotNone(response.data['access'])

    def test_refresh_jwt_token_invalid(self):
        """Test refreshing JWT token with invalid refresh token"""
        refresh_data = {'refresh': 'invalid_token'}
        response = self.client.post(self.refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid JWT token"""
        # Obtain token
        data = {
            'username': self.username,
            'password': self.password
        }
        token_response = self.client.post(self.token_url, data, format='json')
        access_token = token_response.data['access']

        # Access protected endpoint (status list)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(reverse('status-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = self.client.get(reverse('status-list'))

        # Should still work since we have AllowAny in settings
        # If you want to test with authentication required, change this
        self.assertEqual(response.status_code, status.HTTP_200_OK)
