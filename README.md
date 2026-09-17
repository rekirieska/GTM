# GTM
Good Task manager

[Техническое задание](https://docs.google.com/document/d/1ivg931RRbbFaZHiUYeuvgUXxbjUk89q9/edit?usp=sharing&ouid=115162351960228649031&rtpof=true&sd=true)

возможная структура:
GTM/
├── API_CONTRACT.md
├── README.md
├── FAILURE_POINTS.md
├── REPORT.md
├── .gitignore
├── task-service/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── storage.py
│   └── tests/
│       └── test_tasks.py
└── notification-service/
    ├── requirements.txt
    ├── app/
    │   ├── main.py
    │   └── models.py
    └── tests/
        └── test_notifications.py

Функционал:
1. Создание базовой программы.
 - GUI представляет из себя окно на котором сетка задач.
 - Присутствуют три кнопки (создание задачи, удаление задачи, выбор корневой папки)
 - Задачи представляют из себя простой .md файл в папке.
3. Создание дополнительного функционала в виде панели слева с древом корневой папки, где можно просматривать файлы в подпапках.
4. Улучшение интерфейса
