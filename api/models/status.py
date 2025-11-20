from django.db import models


class Status(models.Model):
    """
    Model representing task status.
    Stores status information with name and color.
    """
    # id is auto-created by Django as AutoField primary key
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Status name (e.g., Pending, In Progress, Completed)"
    )
    hexa_color = models.CharField(
        max_length=7,
        help_text="Hexadecimal color code (e.g., #FF5733)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
        ordering = ['name']

    def __str__(self):
        return self.name
