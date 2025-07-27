from typing import Optional

from celery import Celery


celery_app = Celery(
    'app.tasks',
    broker='redis://redis:6379/0',
)


@celery_app.task
def log_event(event_type: str, payload: Optional[dict] = None):
    if event_type == 'create':
        entity_id = payload.get('id') if payload else None
        print(f"📩 Notification sent for entity {entity_id}")
    elif event_type == 'list':
        print("📝 Entities list was requested")
    else:
        print(f"ℹ️ Unknown event: {event_type} | Data: {payload}")
