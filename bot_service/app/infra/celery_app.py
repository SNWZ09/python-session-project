#импортируем celery для создания обработчика фоновых задач
from celery import Celery

#импортируем настройки, так как там наша url для брокера,
#то бишь RabbitMQ, и для бэкенда - Редис
from app.core.config import settings

celery_app = Celery(
            'need_to_answer',
            broker = settings.RABBITMQ_URL,
            backend = settings.REDIS_URL)
            
#из задания копируем строчку, 'чтобы llm_request
#не падала с KeyError'
celery_app.autodiscover_tasks(['app.tasks'])

