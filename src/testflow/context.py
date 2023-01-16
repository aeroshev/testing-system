from contextvars import ContextVar
from uuid import UUID

selected_project_id: ContextVar[UUID] = ContextVar('selected_project_id')