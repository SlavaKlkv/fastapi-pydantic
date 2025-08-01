# FastAPI & Pydantic CRUD

## Описание

Это проект с реализацией CRUD API на FastAPI и Pydantic.  
Все данные хранятся в виде словаря в памяти, которая очищается после перезапуска сервера.  
Поддерживаются все стандартные операции: создание, чтение, обновление, удаление сущности.  
Также есть фильтрация и сортировка через query-параметры.  
Подключены фоновые selery-задачи с брокером Redis.  
Можно запускать как локально, так и через Docker Compose.

---

## Структура проекта

- **app/**
  - **__init__.py**      - Инициализация директории как пакета Python
  - **main.py**          - Реализация эндпоинтов и основной логики FastAPI
  - **schemas.py**       - Pydantic-схемы
  - **storage.py**       - Словарь данных и генерация id
  - **tasks.py**         - Celery-задачи
- **celery_worker.py**   - Код для запуска Celery-воркера
- **docker-compose.yml** - Конфигурация для запуска сети контейнеров
- **Dockerfile**         - Конфигурация сборки и запуска приложения в контейнере
- **README.md**          - Описание проекта и инструкций по запуску
- **requirements.txt**   - Зависимости

---

## Активация и запуск проекта

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/SlavaKlkv/fastapi-pydantic.git
    ```
1. Перейдите в корень проекта:
   ```bash
    cd fastapi-pydantic
   ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
    Для Linux/macOS:
    ```bash
    source venv/bin/activate
    ```
    Для Windows:
    ```bash
    venv\Scripts\activate
    ```
    
### Запуск локально

1. Установите зависимости и redis-сервер:

    ```bash
    pip install -r requirements.txt
    ```
   
    ```bash
    brew install redis
    ```

2. Запустите сервера и selery-воркера

- Запуск uvicorn с автоперезагрузкой после сохранения обновленного кода:
    ```bash
    uvicorn app.main:app --reload
    ```
- Запуск redis-сервера (в другом терминале):
    ```bash
    redis-server
    ```
  
- Запуск воркера (в третьем терминале; он будет выводить сообщения из задач):
    ```bash
    celery -A app.tasks worker --loglevel=info
    ```

### Запуск через Docker Compose

Запуск приложения
    
```bash
   docker compose up
```

Для запуска без пересборки образа с пересозданием контейнеров даже,  
если не было изменений:
```bash
   docker compose up --build --force-recreate
```

Для пересборки образа без использования кеша:
```bash
   docker compose build --no-cache
   docker compose up
```

Остановка всех контейнеров:

- Если запущено обычно:
```bash
   Ctrl + C
```

- Если запущено в фоне:
```bash
   docker compose down
```

### Открыть Swagger UI:
   'http://127.0.0.1:8000/docs'  
   В развернутом поле запроса будет информация о нем - параметры, тело, ответы.  
   Чтобы выполнить запрос,  
   нажмите на `Try it out`, расположенную под описанием справа,  
   и после заполнения (при необходимости) `execute`

---

## Примеры запросов

### Получить список сущностей

**GET** `/entities/`

Parameters  
Можно указать поля фильтрации и сортировки с определенным порядком

Ответ:
```json
[
  {
    "name": "string",
    "value": 27,
    "id": 1
  },
  {
    "name": "entity",
    "value": 33,
    "id": 2
  }
]
```

### Частично обновить сущность

**PATCH** `/entities/{entity_id}`  

Parameters  
**entity_id** `1`  

Тело запроса:
```json
{
  "name": "new_name"
}
```

Ответ:
```json
{
  "name": "new_name",
  "value": 27,
  "id": 1
}
```

---

## Дополнительные инструменты

- Для упорядочивания импортов:
    ```bash
    isort .
    ```

- Для проверки соответствия PEP8:
    ```bash
    flake8 .
    ```
  
---

## Лицензия
MIT
