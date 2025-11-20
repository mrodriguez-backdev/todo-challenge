from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Task, Status as StatusModel
from datetime import datetime, timedelta


class TaskGetTestCase(TestCase):
    """Test case for GET /api/tasks/ endpoint"""

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
        self.status_completed = StatusModel.objects.create(
            name='Completado',
            hexa_color='#10B981'
        )

        # Create test tasks
        self.task1 = Task.objects.create(
            name='Task 1',
            content='Content for task 1',
            status=self.status_pending
        )
        self.task2 = Task.objects.create(
            name='Task 2',
            content='Content for task 2',
            status=self.status_in_progress
        )
        self.task3 = Task.objects.create(
            name='Task 3',
            content='Content for task 3',
            status=self.status_completed
        )

    def test_get_task_list_success(self):
        """Test GET request returns all tasks"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_task_list_contains_correct_data(self):
        """Test GET request returns correct task data"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify task names
        task_names = [task['name'] for task in response.data]
        self.assertIn('Task 1', task_names)
        self.assertIn('Task 2', task_names)
        self.assertIn('Task 3', task_names)

    def test_get_task_detail_success(self):
        """Test GET request for single task"""
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Task 1')
        self.assertEqual(response.data['content'], 'Content for task 1')
        self.assertEqual(response.data['status'], self.status_pending.id)
        self.assertEqual(response.data['status_name'], 'Por Hacer')

    def test_get_task_detail_not_found(self):
        """Test GET request for non-existent task returns 404"""
        url = reverse('task-detail', kwargs={'pk': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status"""
        url = f'{self.url}?status={self.status_pending.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Task 1')

    def test_search_tasks_by_name(self):
        """Test searching tasks by name"""
        url = f'{self.url}?search=Task 1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        task_names = [task['name'] for task in response.data]
        self.assertIn('Task 1', task_names)

    def test_search_tasks_by_content(self):
        """Test searching tasks by content"""
        url = f'{self.url}?search=task 2'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_tasks_by_name(self):
        """Test ordering tasks by name"""
        url = f'{self.url}?ordering=name'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Task 1')
        self.assertEqual(response.data[1]['name'], 'Task 2')
        self.assertEqual(response.data[2]['name'], 'Task 3')

    def test_order_tasks_by_name_descending(self):
        """Test ordering tasks by name descending"""
        url = f'{self.url}?ordering=-name'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Task 3')
        self.assertEqual(response.data[1]['name'], 'Task 2')
        self.assertEqual(response.data[2]['name'], 'Task 1')

    def test_task_response_includes_status_details(self):
        """Test that task response includes status name and color"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_task = response.data[0]
        self.assertIn('status_name', first_task)
        self.assertIn('status_color', first_task)
        self.assertIsNotNone(first_task['status_name'])
        self.assertIsNotNone(first_task['status_color'])
