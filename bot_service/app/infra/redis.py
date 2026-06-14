#импортируем redis.asyncio для работы с redis
import redis.asyncio as redis

#импортируем настройки, так как там наша url для редиса
from app.core.config import settings

redis_client = None

async def get_redis() -> redis.Redis:
    #чтобы не создавать новый клиент на каждый вызов,
    #сделаем переменную глобальной
    #'Важно: не создавать новый клиент на каждый вызов без необходимости'
    #из задания
    global redis_client
    
    #смотрим, создано ли подключение
    #если нет (redis_client = None) - создаем 
    #с помощью url из настроек и возвращаем его
    #так же, пропишем декодирование, чтобы не получалась каша из символов
    #(из урока 2: Оптимизация и интеграция сервисов.
    #Зачем нужен кэш. Использование Redis в качестве кэша)
    if redis_client is None:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
    return redis_client
