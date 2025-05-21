from sqlalchemy import select, update, delete
from database import new_session, TaskOrm
from schemas import STaskAdd, STaskUpdate
from typing import Optional

class TaskRepository:
    @classmethod
    async def add_task(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def get_task(cls, task_id: int) -> Optional[TaskOrm]:
        async with new_session() as session:
            stmt = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(stmt)
            return result.scalars().first()

    @classmethod
    async def get_tasks(cls, sort_by: str = "created_date"):
        async with new_session() as session:
            query = select(TaskOrm).order_by(getattr(TaskOrm, sort_by))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update_task(cls, task_id: int, data: STaskUpdate) -> bool:
        async with new_session() as session:
            update_data = data.model_dump(exclude_unset=True)
            stmt = (
                update(TaskOrm)
                    .where(TaskOrm.id == task_id)
                    .values(**update_data)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def delete_task(cls, task_id: int) -> bool:
        async with new_session() as session:
            stmt = delete(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

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