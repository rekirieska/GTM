id (UUID)
title (string)
description (string)
status (enum: new, in_progress, done),
created_at (ISO8601).

Endpoint 1 (Task Service): POST /api/tasks. Принимает JSON тела задачи (без id и created_at). Возвращает созданную задачу со всеми полями и кодом 201.

Endpoint 2 (Notification Service): POST /api/webhooks/task_created. Принимает JSON объекта Task. Возвращает 200 OK.

Формат сообщения вебхука: Определить точное тело запроса, которое Task Service будет отправлять в Notification Service после успешного создания задачи.
