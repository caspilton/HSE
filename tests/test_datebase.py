import pytest
from sqlalchemy import select
from database import (
    create_tables,
    delete_tables,
    TaskOrm,
    new_session,  # Добавляем импорт
    Model
)


@pytest.mark.asyncio
async def test_table_operations():
    # Создаем и удаляем таблицы
    await delete_tables()
    await create_tables()

    # Проверяем работу сессии
    async with new_session() as session:
        task = TaskOrm(title="Test", priority=1)
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Проверяем запись
        stmt = select(TaskOrm).where(TaskOrm.id == task.id)
        result = await session.execute(stmt)
        fetched_task = result.scalars().first()
        assert fetched_task.title == "Test"

    # Очищаем таблицы после теста
    await delete_tables()