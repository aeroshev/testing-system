from uuid import UUID
from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Project(models.Model):
    """Проект в системе тестирования"""
    id = models.UUIDField(primary_key=True)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    status = ArrayField(
        models.CharField(max_length=128),
        default=list
    )  # type: list[str]
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime
