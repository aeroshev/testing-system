from uuid import UUID, uuid4
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    """Роли пользователей"""
    CHIEF = "Chief", "Начальник"
    TESTER = "Tester", "Тестировщик"
    DEVELOPER = "Developer", "Разработчик"
    ANALYST = "Analyst", "Аналитик"


class User(AbstractUser):
    """Пользователь в системе"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    role = models.CharField(max_length=128, choices=UserRole.choices)  # type: str
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    def __str__(self):
        return f"{self.id} - {UserRole(self.role).label}"

    class Meta:
        db_table = 'users'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_role_valid",
                check=models.Q(role__in=UserRole.values),
            )
        ]
