# Notification Service

Микросервис обработки уведомлений для «Умного планировщика задач».
Подписывается на событие создания задачи и логирует уведомление.

## Endpoint

| Метод | URL | Описание |
|---|---|---|
| POST | /api/webhooks/task_created | Принимает объект Task, возвращает 200 OK |
| GET  | /health | Health-check |

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
