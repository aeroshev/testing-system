from uuid import UUID, uuid4
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager


class UserRole(models.TextChoices):
    """Роли пользователей"""
    CHIEF = "Chief", "Начальник"
    TESTER = "Tester", "Тестировщик"
    DEVELOPER = "Developer", "Разработчик"
    ANALYST = "Analyst", "Аналитик"
    ADMIN = "Admin", "Администратор"


class CustomUserManager(UserManager):
    """Менеджер для управления объектами User"""

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields['role'] = UserRole.ADMIN
        return super(CustomUserManager, self).create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """Пользователь в системе"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    role = models.CharField(max_length=128, choices=UserRole.choices)  # type: str
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    objects = CustomUserManager()

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
