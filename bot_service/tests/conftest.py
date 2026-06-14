#'В этом файле вы подготавливаете тестовую инфраструктуру. 
#Здесь вы должны мокать Redis через fakeredis и патчить get_redis 
#именно там, где он используется, например app.bot.handlers.get_redis.
#Если не сделать патч в правильном месте, тесты будут пытаться подключиться
#к реальному redis:6379.'
#(из задания)
#импорт pytest, patch и fakeredis.aioredis
#взял из урока 5. Production-практики FastAPI. Ошибки и тестирование.
#Запуск интеграционных тестов с помощью TestClient.
import pytest
from unittest.mock import patch
import fakeredis.aioredis

#делаем фикстуру фейкового Редиса
@pytest.fixture
async def fake_redis():
    #делаем фековый клиент Редис по анологии с настоящим из redis.py
    fake_client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    
    #передаем на фейк-клиент и ставим на паузу выполнение функции
    yield fake_client
    
    #закрываем после теста
    await fake_client.close()
    
#    
@pytest.fixture(autouse=True)
def patch_get_redis(fake_redis):
    #патчим в модуле handlers, чтобы бот не лез к реальному redis:6379
    with patch('app.bot.handlers.get_redis', return_value=fake_redis):
        yield
