# FastAPI & Pydantic CRUD

## Описание

Это проект с реализацией CRUD API на FastAPI и Pydantic. Все данные хранятся в памяти в виде словаря, поддерживаются все стандартные операции: создание, чтение, обновление, удаление сущности.

## Структура проекта

- **app/**
  - **__init__.py**     - Инициализация папки как пакета Python
  - **main.py**         - Эндпоинты FastAPI
  - **schemas.py**      - Pydantic-схемы
  - **storage.py**      - Словарь данных и генерация id
- **README.md**         - Описание проекта и инструкций по запуску
- **requirements.txt**  - Зависимости

## Запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/SlavaKlkv/fastapi-pydantic.git
    ```
   Перейдите в корень проекта:
   ```bash
    cd fastapi-pydantic
   ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
    Для Linux/macOS
    ```bash
    source venv/bin/activate
    ```
    Для Windows:
    ```bash
    venv\Scripts\activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Откройте Swagger UI:
   'http://127.0.0.1:8000/docs'

## Пример запроса

---

### Получить список сущностей

**GET** `/entities/`

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

---

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

## Примечания

Все данные удаляются при каждом перезапуске сервера,  
так как используются переменные в памяти.  
Для дополнительной проверки стиля используйте flake8,  
для форматирования импортов - isort.
#