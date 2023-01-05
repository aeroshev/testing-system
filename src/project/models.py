from uuid import UUID, uuid4
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


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
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
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


class ProjectStatus(models.TextChoices):
    """Статусы проекта"""
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
        related_name='projects',
        related_query_name='project',
        on_delete=models.CASCADE
    )  # type: User
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
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


class SuiteStatus(models.TextChoices):
    """Статусы тестового набора"""
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
        related_name='test_suites',
        related_query_name='test_suite',
        on_delete=models.CASCADE
    )  # type: Project
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    def __str__(self):
        return f"{self.id} - {SuiteStatus(self.status).label}"

    class Meta:
        db_table = 'test_suites'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=SuiteStatus.values),
            )
        ]


class RunStatus(models.TextChoices):
    """Статусы запуска"""
    CREATED = "Created", "Создан"
    RUNNING = "Running", "Выполняется"
    SUCCESS = "Success", "Успешно"
    FAILED = "Failed", "Неудачно"


class TestRun(models.Model):
    """Объект запуска тестового набора"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    status = models.CharField(max_length=128, choices=RunStatus.choices)  # type: str
    suite = models.ForeignKey(
        TestSuite,
        null=True,
        related_name='test_runs',
        related_query_name='test_run',
        on_delete=models.SET_NULL
    )  # type: TestSuite
    project = models.ForeignKey(
        Project,
        null=True,
        related_name='test_runs',
        related_query_name='test_run',
        on_delete=models.SET_NULL
    )  # type: Project
    running_by = models.ForeignKey(
        User,
        null=True,
        related_name='test_runs',
        related_query_name='test_run',
        on_delete=models.SET_NULL
    )  # type: User
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    class Meta:
        db_table = 'test_runs'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=RunStatus.values),
            )
        ]


class TestCase(models.Model):
    """Тестовый набор"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    executed_code = models.IntegerField()  # type: int
    conditions = ArrayField(
        models.CharField(max_length=512),
        default=list
    )  # type: list[str]
    steps = ArrayField(
        models.CharField(max_length=512),
        default=list
    )  # type: list[str]
    test_suites = models.ManyToManyField(
        TestSuite,
        related_name='test_cases',
        related_query_name='test_case'
    )  # type: list[TestSuite]
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    class Meta:
        db_table = 'test_cases'


class Report(models.Model):
    """Отчёты о тестировании"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    description = models.TextField()  # type: str
    test_run = models.ForeignKey(
        TestRun,
        null=True,
        related_name='reports',
        related_query_name='report',
        on_delete=models.SET_NULL
    )  # type: TestRun
    created_at = models.DateTimeField(auto_created=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    class Meta:
        db_table = 'reports'
