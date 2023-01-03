from uuid import UUID, uuid4
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    CHIEF = "Chief", "Начальник"
    TESTER = "Tester", "Тестировщик"
    DEVELOPER = "Developer", "Разработчик"
    ANALYST = "Analyst", "Аналитик"


class User(AbstractUser):
    """Пользователь в системе"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    role = models.CharField(max_length=128, choices=UserRole.choices)  # type: str
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    def __str__(self):
        return f"{self.id} - {UserRole(self.role).label}"

    class Meta:
        db_table = 'user'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_role_valid",
                check=models.Q(role__in=UserRole.values),
            )
        ]


class ProjectStatus(models.TextChoices):
    CREATED = "Created", "Создан"
    EDITED = "Edited", "Редактируется"
    FINISHED = "Finished", "Завершён"


class Project(models.Model):
    """Проект в системе тестирования"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    status = models.CharField(max_length=128, choices=ProjectStatus.choices)  # type: str
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  # type: User
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    def __str__(self):
        return f"{self.id} - {ProjectStatus(self.status).label}"

    class Meta:
        db_table = 'project'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=ProjectStatus.values),
            )
        ]


class SuiteStatus(models.TextChoices):
    CREATED = "Created", "Создан"
    EDITED = "Edited", "Редактируется"
    FINISHED = "Finished", "Завершён"


class TestSuite(models.Model):
    """Тестовый набор"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    status = models.CharField(max_length=128, choices=SuiteStatus.choices)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )  # type: Project
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    def __str__(self):
        return f"{self.id} - {SuiteStatus(self.status).label}"

    class Meta:
        db_table = 'test_suite'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=SuiteStatus.values),
            )
        ]
