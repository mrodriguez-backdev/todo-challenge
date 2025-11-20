from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Task, Status as StatusModel


class TaskPostTestCase(TestCase):
    """Test case for POST /api/tasks/ endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.url = reverse('task-list')

        # Create test statuses
        self.status_pending = StatusModel.objects.create(
            name='Por Hacer',
            hexa_color='#6B7280'
        )
        self.status_in_progress = StatusModel.objects.create(
            name='En Progreso',
            hexa_color='#3B82F6'
        )

    def test_create_task_success(self):
        """Test creating a task with valid data"""
        data = {
            'name': 'New Task',
            'content': 'This is a new task',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Task')
        self.assertEqual(response.data['content'], 'This is a new task')
        self.assertEqual(response.data['status'], self.status_pending.id)

        # Verify task was created in database
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_create_task_with_status_details(self):
        """Test that created task response includes status details"""
        data = {
            'name': 'Task with Status Details',
            'content': 'Testing status details',
            'status': self.status_in_progress.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('status_name', response.data)
        self.assertIn('status_color', response.data)
        self.assertEqual(response.data['status_name'], 'En Progreso')
        self.assertEqual(response.data['status_color'], '#3B82F6')

    def test_create_task_missing_name(self):
        """Test creating task without name returns 400"""
        data = {
            'content': 'Task without name',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_task_missing_content(self):
        """Test creating task without content returns 400"""
        data = {
            'name': 'Task without content',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

    def test_create_task_missing_status(self):
        """Test creating task without status returns 400"""
        data = {
            'name': 'Task without status',
            'content': 'This task has no status'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_create_task_invalid_status(self):
        """Test creating task with non-existent status ID returns 400"""
        data = {
            'name': 'Task with invalid status',
            'content': 'Testing invalid status',
            'status': 9999
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_empty_name(self):
        """Test creating task with empty name returns 400"""
        data = {
            'name': '',
            'content': 'Task with empty name',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_task_empty_content(self):
        """Test creating task with empty content returns 400"""
        data = {
            'name': 'Task with empty content',
            'content': '',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

    def test_create_multiple_tasks(self):
        """Test creating multiple tasks"""
        data1 = {
            'name': 'Task 1',
            'content': 'Content 1',
            'status': self.status_pending.id
        }
        data2 = {
            'name': 'Task 2',
            'content': 'Content 2',
            'status': self.status_in_progress.id
        }

        response1 = self.client.post(self.url, data1, format='json')
        response2 = self.client.post(self.url, data2, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Verify both tasks exist
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_with_long_name(self):
        """Test creating task with long name"""
        long_name = 'A' * 200  # Max length is 200
        data = {
            'name': long_name,
            'content': 'Task with long name',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_with_too_long_name(self):
        """Test creating task with name exceeding max length returns 400"""
        too_long_name = 'A' * 201  # Max length is 200
        data = {
            'name': too_long_name,
            'content': 'Task with too long name',
            'status': self.status_pending.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
