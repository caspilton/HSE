def test_create_task(test_client):
    response = test_client.post("/tasks", json={
        "title": "Test",
        "priority": 1,
        "status": "в ожидании"  # Используем значение вместо имени константы
    })
    assert response.status_code == 200
    assert response.json()["status"] == "в ожидании"



def test_create_task_invalid_data(test_client):
    # Пустой title
    response = test_client.post("/tasks", json={"priority": 1})
    assert response.status_code == 422
    assert "title" in response.text

    # Приоритет меньше 1
    response = test_client.post("/tasks", json={"title": "Test", "priority": 0})
    assert response.status_code == 422

    # Неверный статус
    response = test_client.post("/tasks", json={
        "title": "Test",
        "priority": 1,
        "status": "invalid_status"
    })
    assert response.status_code == 422

def test_create_task_with_max_values(test_client):
    # 255 символов для title
    long_title = "T" * 255
    response = test_client.post("/tasks", json={
        "title": long_title,
        "priority": 1
    })
    assert response.status_code == 200

    # 256 символов - должно падать
    long_title = "T" * 256
    response = test_client.post("/tasks", json={
        "title": long_title,
        "priority": 1
    })
    assert response.status_code == 422

def test_invalid_data_types(test_client):
    # Строка вместо числа для приоритета
    response = test_client.post("/tasks", json={
        "title": "Test",
        "priority": "high"
    })
    assert response.status_code == 422

    # Число вместо строки для статуса
    response = test_client.patch("/tasks/1", json={"status": 123})
    assert response.status_code == 422