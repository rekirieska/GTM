from fastapi.testclient import TestClient
# Импортируем app из файла tasks_service.py
from tasks_service import app

client = TestClient(app)

def test_create_task_success():
    payload = {"title": "Купить хлеб", "description": "Зайти в магазин", "status": "new"}
    response = client.post("/api/tasks", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Купить хлеб"
    assert data["description"] == "Зайти в магазин"
    assert data["status"] == "new"
    assert "created_at" in data

def test_create_task_validation_error():
    payload = {"title": "", "description": "Тест"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 422
