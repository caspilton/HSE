from fastapi.testclient import TestClient
from fastapi import status
from main import app
import pytest

client = TestClient(app)


def test_full_crud_flow(test_client):
    # Создание
    response = test_client.post("/tasks", json={
        "title": "Test",
        "priority": 1
    })
    assert response.json()["status"] == "в ожидании"  # Проверка дефолтных значений
    task_id = response.json()["id"]

    # Чтение
    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert any(task["id"] == task_id for task in response.json())

    # Обновление
    response = test_client.patch(f"/tasks/{task_id}", json={"title": "Updated"})
    assert response.status_code == 200

    # Удаление
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

def test_invalid_sort_parameter():
    response = client.get("/tasks?sort_by=invalid_field")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_top_priority_tasks():
    response = client.get("/tasks/top?limit=3")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) <= 3

def test_update_nonexistent_task(test_client):
    response = test_client.patch("/tasks/999", json={"title": "Updated"})
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]

def test_delete_nonexistent_task(test_client):
    response = test_client.delete("/tasks/999")
    assert response.status_code == 404

def test_sql_injection_attempt(test_client):
    # Попытка SQL-инъекции через параметр сортировки
    response = test_client.get("/tasks?sort_by=;DROP TABLE tasks;--")
    assert response.status_code == 400

    # Инъекция через поисковый запрос
    response = test_client.get("/tasks/search?query=' OR 1=1;--")
    assert response.status_code == 200  # Должен безопасно обработать
    assert len(response.json()) == 0    # Но не возвращать данные

def test_get_empty_tasks_list(test_client):
    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 0  # После очистки БД в начале каждого теста