from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import Field, field_validator

class TaskStatus(str, Enum):
    PENDING = "в ожидании"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"

class STaskAdd(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: int = Field(1, ge=1, le=5)

    @field_validator('status')
    def validate_status(cls, v):
        return v.value if isinstance(v, TaskStatus) else v

class STaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None

class STask(STaskAdd):
    id: int
    created_date: datetime

class STaskId(BaseModel):
    id: int