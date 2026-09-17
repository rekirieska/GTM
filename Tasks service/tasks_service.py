import logging
import uuid
from datetime import datetime, timezone
from enum import Enum
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TaskService")

app = FastAPI(title="Task Service")
tasks_db = {} 

# Имитация доступности базы данных для обработки Точки Отказа 1
IS_DATABASE_AVAILABLE = True 

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"

# Схема входящего запроса (Endpoint 1) — без id и created_at
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)  # Обязательное поле
    description: str = Field(default="")   # По умолчанию пустая строка
    status: TaskStatus = Field(default=TaskStatus.NEW) # По умолчанию new

# Полная схема ответа Task со всеми полями
class TaskResponse(TaskCreate):
    id: uuid.UUID
    created_at: str

NOTIFICATION_URL = "http://localhost:8001/api/webhooks/task_created"

# Обработчик ошибки валидации (Код 422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Не прошла валидация (например, пустой title)"}
    )
# Импортируйте JSONDecodeError в самый верх файла, если его там нет:
from json import JSONDecodeError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Проверяем, вызвана ли ошибка именно сломанным синтаксисом JSON
    for error in exc.errors():
        if error.get("type") == "json_invalid":
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Некорректный JSON (синтаксическая ошибка)"}
            )
            
    # Во всех остальных случаях валидации (например, пустой title) возвращаем 422
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Не прошла валидация полей"}
    )


@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate):
    # Точка отказа 1: Хранилище задач недоступно -> Возврат 500
    if not IS_DATABASE_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Хранилище задач недоступно"
        )
    
    # Автогенерация системных полей на сервере
    task_id = uuid.uuid4()
    created_at_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    new_task = {
        "id": str(task_id),
        "title": task_in.title,
        "description": task_in.description,
        "status": task_in.status.value,
        "created_at": created_at_iso
    }
    tasks_db[str(task_id)] = new_task
    logger.info(f"Задача {task_id} успешно сохранена в in-memory БД.")
    # Отправка вебхука в Notification Service
    try:
        async with httpx.AsyncClient() as client:
            # Отправляем полный объект по формату сообщения вебхука
            response = await client.post(NOTIFICATION_URL, json=new_task, timeout=2.0)
            if response.status_code != 200:
                logger.warning(f"Notification Service вернул код {response.status_code}")
    except (httpx.RequestError, httpx.TimeoutException) as exc:
        # Точка отказа 2: Notification Service недоступен -> Логируем, но код 201 возвращается клиенту
        logger.error(f"Notification Service недоступен: {exc}. Задача всё равно создана в БД.")

    return new_task
