from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_webhook_accepts_valid_task():
    '''Основной сценарий: валидное событие - 200 OK'''
    payload = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Купить хлеб",
        "description": "Зайти в магазин",
        "status": "new",
        "created_at": "2026-09-14T10:30:00Z",
    }
    response = client.post("/api/webhooks/task_created", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}

def test_webhook_rejects_invalid_body():
    '''Сценарий ошибки: нет обязательных полей - 422'''
    response = client.post("/api/webhooks/task_created", json={"title": "Без id"})
    assert response.status_code == 422

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
