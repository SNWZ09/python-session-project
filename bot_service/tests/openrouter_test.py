#'Интеграционные тесты должны проверять клиента OpenRouter,
#но без реального доступа к интернету. Поэтому здесь используется respx.'
#(из задания)
import respx

#pytest, настройки и функция вызова openrouter
import pytest
from app.core.config import settings
from app.services.openrouter_client import call_openrouter_client

#импорт httpx, так как функция опенрутера использует httpx.AsyncClient() 
import httpx

#делаем тесты асинхронными
@pytest.mark.asyncio

#добавляем respx, чтобы перехватывать интернет
@respx.mock
async def test_call_openrouter_client():
    
    #'Вы поднимаете мок-роут на POST https://openrouter.ai/api/v1/chat/completions'
    #из задания
    url = f'settings.OPENROUTER_BASE_URL}/chat/completions'
    
    #создаем фековый ответ
    fake_openrouter_response = {'choices': [
            {
                'message': {
                    'content': '*Глубоко дышит* Угабуга донкиконг... забавно. *Dies from cringe*'
                }
            }
        ]
    }
    
    #как сделать лже-ответ подсмотрел
    #Прошу прощения, было суперсложно разобраться, как сюда вообще respx впихнуть
    #по факту происходит следующее:
    #эта строчка закрепляет, что если кто-то делает запрос на тот url, что мы указали - этот
    #запрос ловится, потом в return_value помещается муляж ответа fake_openrouter_response
    #и статус-код 200, мол, всё прошло хорошо
    mock_route = respx.post(url).mock(return_value=httpx.Response(200, json=fake_response_json))
    
    #теперь вызываем call_openrouter_client, который попытается выйти в сеть
    openrouter_client_result = await call_openrouter_client('Угабуга донкиконг')
    
    #теперь проверяем, что запрос пытался уйти в сеть
    #'assert_called() — проверяет, что функция была вызвана хотя бы раз.'
    #из материалов на платформе
    #урок 4. Production-практики FastAPI. Ошибки и тестирование.
    #Написание модульных тестов для FastAPI. Мокинг внешних зависимостей в unit тестах.
    assert mock_route.called
    
    #и, как сигнал, что в сеть выйти не получилось
    #openrouter_client_result должен быть равен контенту из fake_openrouter_response
    assert openrouter_client_result == '*Глубоко дышит* Угабуга донкиконг... забавно. *Dies from cringe*'
