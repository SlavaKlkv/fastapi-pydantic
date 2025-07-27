from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from starlette import status

from .schemas import Entity, EntityCreate, EntityUpdate
from .storage import entities, next_id
from .tasks import log_event


app = FastAPI()


def get_entity_or_404(entity_id: int) -> Entity:
    """Получение сущности или выброс ошибки."""
    if entity_id not in entities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Entity not found'
        )
    return entities[entity_id]


@app.get(
    '/entities/',
    response_model=list[Entity],
    description='Получить список всех сущностей'
)
def list_entities(
    name: Optional[str] = Query(
        None, description='Фильтрация по имени'
    ),
    value: Optional[int] = Query(
        None, description='Фильтрация по значению'
    ),
    sort: Optional[str] = Query(
        None, description='Поле для сортировки: name или value'
    ),
    order: Optional[str] = Query(
        'asc', description='Порядок сортировки: '
                           'asc (по возрастанию) или desc (по убыванию)'
    )
):
    results = list(entities.values())
    if name is not None:
        results = [e for e in results if e.name == name]
    if value is not None:
        results = [e for e in results if e.value == value]
    if sort is not None and sort in ('name', 'value'):
        results = sorted(
            results, key=lambda e: getattr(e, sort), reverse=order == 'desc'
        )
    log_event.delay('list')
    return results


@app.get(
    '/entities/{entity_id}',
    response_model=Entity,
    description='Получить одну сущность по её ID'
)
def get_entity(entity_id: int):
    return get_entity_or_404(entity_id)


@app.post(
    '/entities/',
    response_model=Entity,
    description='Создать новую сущность'
)
def create_entity(entity: EntityCreate):
    eid = next_id()
    new_entity = Entity(id=eid, **entity.model_dump())
    entities[eid] = new_entity
    log_event.delay('create', new_entity.model_dump())
    return new_entity


@app.patch(
    '/entities/{entity_id}',
    response_model=Entity,
    description='Частично обновить данные сущности по её ID'
)
def update_entity(entity_id: int, entity_update: EntityUpdate):
    original = get_entity_or_404(entity_id)
    update_data = {
        k: v for k, v in entity_update.model_dump().items() if v is not None
    }
    updated = original.model_copy(update=update_data)
    entities[entity_id] = updated
    return updated


@app.delete(
    '/entities/{entity_id}',
    response_model=Entity,
    description='Удалить сущность по её ID'
)
def delete_entity(entity_id: int):
    get_entity_or_404(entity_id)
    return entities.pop(entity_id)
