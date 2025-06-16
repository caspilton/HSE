from fastapi import APIRouter, Depends, HTTPException
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskId, STaskUpdate, TaskStatus
from fastapi import HTTPException, status

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)

@router.post("", response_model=STask)
async def add_task(task: STaskAdd):
    task_data = task.model_dump()
    if isinstance(task_data["status"], TaskStatus):
        task_data["status"] = task_data["status"].value

    new_task_id = await TaskRepository.add_task(STaskAdd(**task_data))
    return await TaskRepository.get_task(new_task_id)

@router.get("", response_model=list[STask])
@router.get("", response_model=list[STask])
async def get_tasks(sort_by: str = "created_date"):
    valid_fields = ["title", "status", "created_date", "priority"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by parameter. Allowed: {valid_fields}"
        )
    return await TaskRepository.get_tasks(sort_by)

@router.patch("/{task_id}")
async def update_task(task_id: int, task_data: STaskUpdate):
    is_updated = await TaskRepository.update_task(task_id, task_data)
    if not is_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return {"ok": True}

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    is_deleted = await TaskRepository.delete_task(task_id)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return {"ok": True}

@router.get("/search", response_model=list[STask])
async def search_tasks(query: str):
    return await TaskRepository.search_tasks(query)

@router.get("/top", response_model=list[STask])
async def get_top_priority_tasks(limit: int = 5):
    return await TaskRepository.get_top_priority_tasks(limit)