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
from unittest.mock import patch
import httpx

def test_create_task_when_notification_service_fails():
    payload = {
        "title": "Задача при падении вебхука",
        "description": "Проверка отказоустойчивости",
        "status": "new"
    }
    
    # Имитируем падение сети (ошибку httpx) при отправке вебхука
    with patch("httpx.AsyncClient.post", side_effect=httpx.RequestError("Сервис уведомлений недоступен")):
        response = client.post("/api/tasks", json=payload)
        
        # Проверяем, что Task Service НЕ упал, а вернул 201 по контракту!
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Задача при падении вебхука"
