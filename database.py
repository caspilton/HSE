from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from enum import Enum

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TaskStatusEnum(Enum):
    PENDING = "в ожидании"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    status: Mapped[str] = mapped_column(default=TaskStatusEnum.PENDING.value)
    priority: Mapped[int] = mapped_column(default=1)
    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

@classmethod
async def get_top_priority_tasks(cls, limit: int):
    if limit <= 0:
        return []
    async with new_session() as session:
        stmt = select(TaskOrm).order_by(
            TaskOrm.priority.desc()
        ).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

@classmethod
async def search_tasks(cls, search_query: str):
    if not search_query.strip():
        return []
    async with new_session() as session:
        stmt = select(TaskOrm).where(
            (TaskOrm.title.ilike(f"%{search_query}%")) |
            (TaskOrm.description.ilike(f"%{search_query}%"))
        )
        result = await session.execute(stmt)
        return result.scalars().all()