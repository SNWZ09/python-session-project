#импортируем celery для создания обработчика фоновых задач
from celery import Celery

#импортируем настройки, так как там наша url для брокера,
#то бишь RabbitMQ, и для бэкенда - Редис
from app.core.config import settings

celery_app = Celery(
            'worker',
            broker = settings.RABBITMQ_URL,
            backend = settings.REDIS_URL,
            include = ['app.tasks.llm_tasks'])
