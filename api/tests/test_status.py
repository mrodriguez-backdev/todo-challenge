from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Status as StatusModel


class StatusGetTestCase(TestCase):
    """Test case for GET /api/status/ endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.url = reverse('status-list')

        # Create and authenticate user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # Create test status records
        self.status1 = StatusModel.objects.create(
            name='Por Hacer',
            hexa_color='#6B7280'
        )
        self.status2 = StatusModel.objects.create(
            name='En Progreso',
            hexa_color='#3B82F6'
        )
        self.status3 = StatusModel.objects.create(
            name='Completado',
            hexa_color='#10B981'
        )

    def test_get_status_list_success(self):
        """Test GET request returns all status records"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_status_list_contains_correct_data(self):
        """Test GET request returns correct status data"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify first status
        status_names = [s['name'] for s in response.data]
        self.assertIn('Por Hacer', status_names)
        self.assertIn('En Progreso', status_names)
        self.assertIn('Completado', status_names)

    def test_get_status_detail_success(self):
        """Test GET request for single status record"""
        url = reverse('status-detail', kwargs={'pk': self.status1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Por Hacer')
        self.assertEqual(response.data['hexa_color'], '#6B7280')

    def test_get_status_detail_not_found(self):
        """Test GET request for non-existent status returns 404"""
        url = reverse('status-detail', kwargs={'pk': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
