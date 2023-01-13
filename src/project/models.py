from uuid import UUID, uuid4
from datetime import datetime

from django.db import models

from user.models import User


class ProjectStatus(models.TextChoices):
    """Статусы проекта"""
    CREATED = "Created", "Создан"
    EDITED = "Edited", "Редактируется"
    FINISHED = "Finished", "Завершён"


class Project(models.Model):
    """Проект в системе тестирования"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    description = models.TextField()  # type: str
    status = models.CharField(max_length=128, choices=ProjectStatus.choices)  # type: str
    manager = models.ForeignKey(
        User,
        related_name='projects',
        related_query_name='project',
        on_delete=models.CASCADE
    )  # type: User
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    def __str__(self):
        return f"{self.id} - {ProjectStatus(self.status).label}"

    class Meta:
        db_table = 'projects'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=ProjectStatus.values),
            )
        ]
