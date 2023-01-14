from datetime import datetime
from uuid import UUID, uuid4

from django.contrib.postgres.fields import ArrayField
from django.db import models

from project.models import Project
from user.models import User


class SuiteStatus(models.TextChoices):
    """Статусы тестового набора"""
    CREATED = "Created", "Создан"
    EDITED = "Edited", "Редактируется"
    FINISHED = "Finished", "Завершён"


class TestSuite(models.Model):
    """Тестовый набор"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    status = models.CharField(
        max_length=128,
        choices=SuiteStatus.choices,
        default=SuiteStatus.CREATED
    )  # type: str
    project = models.ForeignKey(
        Project,
        related_name='test_suites',
        related_query_name='test_suite',
        on_delete=models.CASCADE
    )  # type: Project
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
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
    status = models.CharField(
        max_length=128,
        choices=RunStatus.choices,
        default=RunStatus.CREATED
    )  # type: str
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
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
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
        null=True,
        related_name='test_cases',
        related_query_name='test_case'
    )  # type: list[TestSuite]
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    class Meta:
        db_table = 'test_cases'


class ReportStatus(models.TextChoices):
    """Статусы отчёта о тестировании"""
    NOT_LOADED = "Not loaded", "Не загружен"
    LOADED = "Loaded", "Загружен"
    APPROVED = "Approved", "Утвержден"
    EDITED = "Edited", "Редактируется"


def user_directory_path(instance: 'Report', filename: str) -> str:
    return f'reports/user_{instance.user.id}/{filename}'


class Report(models.Model):
    """Отчёты о тестировании"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # type: UUID
    name = models.CharField(max_length=512)  # type: str
    description = models.TextField()  # type: str
    status = models.CharField(
        max_length=128,
        choices=ReportStatus.choices,
        default=ReportStatus.NOT_LOADED
    )  # type: str
    test_run = models.ForeignKey(
        TestRun,
        null=True,
        related_name='reports',
        related_query_name='report',
        on_delete=models.SET_NULL
    )  # type: TestRun
    file = models.FileField(
        null=True,
        blank=True,
        upload_to=user_directory_path
    )
    created_at = models.DateTimeField(auto_now_add=True)  # type: datetime
    changed_at = models.DateTimeField(auto_now=True)  # type: datetime

    class Meta:
        db_table = 'reports'
