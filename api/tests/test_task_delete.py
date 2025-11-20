from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Task, Status as StatusModel


class TaskDeleteTestCase(TestCase):
    """Test case for DELETE /api/tasks/{id}/ endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create test statuses
        self.status_pending = StatusModel.objects.create(
            name='Por Hacer',
            hexa_color='#6B7280'
        )
        self.status_completed = StatusModel.objects.create(
            name='Completado',
            hexa_color='#10B981'
        )

        # Create test tasks
        self.task1 = Task.objects.create(
            name='Task to delete',
            content='This task will be deleted',
            status=self.status_pending
        )
        self.task2 = Task.objects.create(
            name='Another task',
            content='This task should remain',
            status=self.status_completed
        )

    def test_delete_task_success(self):
        """Test deleting a task successfully"""
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify task was deleted from database
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_delete_task_not_found(self):
        """Test deleting non-existent task returns 404"""
        url = reverse('task-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_doesnt_affect_other_tasks(self):
        """Test deleting one task doesn't affect other tasks"""
        initial_count = Task.objects.count()
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify only one task was deleted
        self.assertEqual(Task.objects.count(), initial_count - 1)

        # Verify task2 still exists
        self.assertTrue(Task.objects.filter(id=self.task2.id).exists())

    def test_delete_already_deleted_task(self):
        """Test deleting an already deleted task returns 404"""
        url = reverse('task-detail', kwargs={'pk': self.task1.id})

        # First deletion
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete again
        response2 = self.client.delete(url)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_by_id_string(self):
        """Test deleting task with string ID (should still work)"""
        url = reverse('task-detail', kwargs={'pk': str(self.task1.id)})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_get_deleted_task_returns_404(self):
        """Test that getting a deleted task returns 404"""
        url = reverse('task-detail', kwargs={'pk': self.task1.id})

        # Delete the task
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to get the deleted task
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_multiple_tasks_sequentially(self):
        """Test deleting multiple tasks one by one"""
        # Create additional tasks
        task3 = Task.objects.create(
            name='Task 3',
            content='Content 3',
            status=self.status_pending
        )
        task4 = Task.objects.create(
            name='Task 4',
            content='Content 4',
            status=self.status_pending
        )

        initial_count = Task.objects.count()

        # Delete task3
        url3 = reverse('task-detail', kwargs={'pk': task3.id})
        response3 = self.client.delete(url3)
        self.assertEqual(response3.status_code, status.HTTP_204_NO_CONTENT)

        # Delete task4
        url4 = reverse('task-detail', kwargs={'pk': task4.id})
        response4 = self.client.delete(url4)
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)

        # Verify both were deleted
        self.assertEqual(Task.objects.count(), initial_count - 2)
        self.assertFalse(Task.objects.filter(id=task3.id).exists())
        self.assertFalse(Task.objects.filter(id=task4.id).exists())

    def test_delete_task_with_invalid_id_format(self):
        """Test deleting task with invalid ID format returns 404"""
        url = '/api/tasks/invalid_id/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
