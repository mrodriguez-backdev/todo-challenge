from django.db import models
from .status import Status


class Task(models.Model):
    """
    Model representing a task.
    Each task has a name, content, status, and timestamps.
    """
    name = models.CharField(
        max_length=200,
        help_text="Task name or title"
    )
    content = models.TextField(
        help_text="Detailed description of the task"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        help_text="Current status of the task"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
