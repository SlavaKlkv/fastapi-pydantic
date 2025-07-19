from fastapi import FastAPI, HTTPException
from starlette import status

from .schemas import Entity, EntityCreate, EntityUpdate
from .storage import entities, next_id

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
def list_entities():
    return list(entities.values())


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
