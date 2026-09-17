from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from enum import Enum
import logging


'''Логирование в файл и в консоль'''
LOG_FILE = "notifications.log"

class TaskStatus(str, Enum):
    '''Статус задачи — должен совпадать с Task Service.'''
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"

logger = logging.getLogger("notification_service")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[NOTIFY] %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

''' Приложение '''
app = FastAPI(title="Notification Service")

class TaskEvent(BaseModel):
    """Событие создания задачи приходит от Task Service."""
    id: str
    title: str
    description: str = ""
    status: TaskStatus
    created_at: str

@app.post("/api/webhooks/task_created")
def task_created(task: TaskEvent):
    ''' Принимает событие создания задачи. Возвращает 200 OK '''
    try:
        logger.info(
            "Получено событие: task_id=%s, title='%s', status=%s",
            task.id, task.title, task.status,
        )
        # здесь могла бы быть реальная отправка (email, push и т.д.)
        return {"status": "received"}

    except Exception as e:
        ''' Локальная точка отказа №2 — ошибка при обработке '''
        logger.error("Ошибка обработки события task_id=%s: %s", task.id, e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": "Обработка не удалась"},
        )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    '''Локальная точка отказа №1 — невалидное тело запроса'''
    logger.warning("Невалидное тело запроса: %s", exc)
    return JSONResponse(
        status_code=422,
        content={"status": "error", "detail": "Невалидное тело запроса"},
    )

@app.get("/health")
def health():
    '''Простой health-check'''
    return {"status": "ok"}
