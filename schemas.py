from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "в ожидании"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"

class STaskAdd(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1

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