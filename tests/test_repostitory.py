from database import TaskOrm  # Добавьте импорт
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from repository import TaskRepository
from schemas import STaskAdd, STaskUpdate, TaskStatus


@pytest.mark.asyncio
async def test_add_task_success(mocker):
    mock_task = mocker.MagicMock()
    mock_task.id = 1

    mock_session = AsyncMock()
    mock_session.add = mocker.MagicMock()
    mock_session.flush = AsyncMock()
    mock_session.commit = AsyncMock()

    mock_session_ctx = mocker.MagicMock()
    mock_session_ctx.__aenter__.return_value = mock_session
    mock_session_ctx.__aexit__.return_value = None

    mocker.patch("repository.new_session", return_value=mock_session_ctx)

    mocker.patch("repository.TaskOrm", return_value=mock_task)

    task_data = STaskAdd(
        title="Test",
        description="Test",
        status=TaskStatus.PENDING,
        priority=1
    )

    task_id = await TaskRepository.add_task(task_data)
    assert task_id == 1
    mock_session.add.assert_called_once_with(mock_task)

@pytest.mark.asyncio
async def test_update_task_not_found(mocker):
    mock_session = AsyncMock()
    mock_session.execute.return_value.rowcount = 0

    mocker.patch("database.new_session", return_value=mock_session)

    is_updated = await TaskRepository.update_task(999, STaskUpdate(title="Updated"))
    assert is_updated is False  # Проверяем возврат False вместо исключения


@pytest.mark.asyncio
async def test_search_tasks(mocker):
    mock_task = TaskOrm(title="Test", description="Test search")

    mock_result = mocker.MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_task]

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    mock_session_ctx = mocker.MagicMock()
    mock_session_ctx.__aenter__.return_value = mock_session

    mocker.patch("repository.new_session", return_value=mock_session_ctx)

    tasks = await TaskRepository.search_tasks("test")
    assert len(tasks) == 1
    assert tasks[0].title == "Test"

@pytest.mark.asyncio
async def test_get_top_priority_with_invalid_limit():
    tasks = await TaskRepository.get_top_priority_tasks(limit=-5)
    assert len(tasks) == 0  # Должен возвращать пустой список

@pytest.mark.asyncio
async def test_search_empty_query():
    tasks = await TaskRepository.search_tasks("")
    assert len(tasks) == 0  # Пустой запрос - нет результатов


@pytest.mark.asyncio
async def test_create_duplicate_tasks():
    task_data = STaskAdd(title="Unique Task", priority=1)
    await TaskRepository.add_task(task_data)

    # Пытаемся создать дубликат
    duplicate_id = await TaskRepository.add_task(task_data)
    assert isinstance(duplicate_id, int)  # Разрешаем дубликаты, если нет ограничений в БД