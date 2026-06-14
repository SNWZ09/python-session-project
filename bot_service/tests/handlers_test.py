#импорт pytest
import pytest

#импорт AsyncMock (из урока 6. Production-практики FastAPI. Ошибки и тестирование.
#Асинхронное тестирование FastAPI.) для фейковых сообщений 
#patch для заглушки Celery
from unittest.mock import AsyncMock, patch

#поскольку нужны фейковые сообщения - импорт Message и Chat
from aiogram.types import Message, Chat

#для работы с токенами
from jose import jwt

#импорт настроек и функции user_text_message из handlers.py
#тк именно в ней у меня и происходит обработка токена
from app.core.config import settings
from app.bot.handlers import user_text_message

#создаем фейк-сообщение
def create_fake_message(text: str, chat_id: int = 255981) -> Message:
    
    #говорим, что этот мок-объект является сообщением
    msg = AsyncMock(spec=Message)
    
    #записываем поле текст
    msg.text = text
    
    msg.chat = AsyncMock(spec=Chat)
    msg.chat.id = chat_id
    return msg
    
#первый тест
#проверяем, что бот принимает и сохраняет токен в fake_redis
@pytest.mark.asyncio
async def test_handler_saves_token(fake_redis):

    #генерируем токен для теста 
    test_payload = {'sub': '255981', 'role': 'user'}
    token = jwt.encode(test_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    
    #создаем фейковое сообщение функцией fake_message
    #в которое зашиваем токен
    fake_message = create_fake_message(text=token, chat_id=255981)
    
    #запускаем обработчик
    await user_text_message(fake_message)
    
    #проверяем, что запись в fake_redis появилась
    #'проверяете, что токен действительно сохранился в 
    #fake redis под ключом вида token:<tg_user_id>. '
    #(из задания)
    auth_statement = 'is_user_confirmed_token:255981'
    fake_redis_value = await fake_redis.get(auth_statement)
    
    #проходит тест, если fake_redis_value истина
    assert fake_redis_value == 'true'
    

#второй тест
#'если токена нет - появляется сообщение об ошибке
#Затем вы пишете тест, что если токена нет, то при обычном 
#тексте бот не вызывает Celery и отвечает сообщением об отсутствии токена.'
#(из задания)
@pytest.mark.asyncio
async def test_handler_no_token_message(fake_redis):

    #опять создаем фейк-месседж с рандомным текстом
    fake_message = create_fake_message(text='Это 100% токен, поверь мне. Человек никогда не врет', chat_id=255981)
    
    #опять запускаем обработчик
    await user_text_message(fake_message)
    
    #бот ответил сообщение об ошибке
    #(из урока 4. Production-практики FastAPI. Ошибки и тестирование.
    #Написание модульных тестов для FastAPI. Мокинг внешних зависимостей в unit тестах.
    #assert_called_once() — проверяет, что функция была вызвана ровно один раз.)
    fake_message.answer.assert_called_once()
    
    #смотрим текст ответа, проверяем, что там есть слова,
    #которые обработчик выдает, когда с токеном что-то не так
    #args получит кортеж со всеми строками
    #Прошу прощения, тут нейросеть подсказала, как нормально получить ответ бота
    args, _ = fake_message.answer.call_args
    assert 'С токеном что-то не та' in args[0]


#третий тест
#'тест, что если токен сохранён, то при обычном тексте бот
#вызывает llm_request.delay(...) и передаёт туда правильные аргументы,
#а пользователю отправляется сообщение “Запрос принят” или аналогичное.
#В этом тесте важно мокать llm_request.delay через pytest-mock, 
#иначе тест действительно попробует отправить задачу в RabbitMQ.'
#учитывая последнюю строчку - будем использовать патч на llm_request.delay
@pytest.mark.asyncio
@patch('app.bot.handlers.llm_request.delay')
async def test_handler_authorized_calls_celery(mock_delay, fake_redis):

    #опять создаем фейк-месседж с рандомным текстом
    fake_message = create_fake_message(text='Угабуга донкиконг', chat_id=255981)
    
    #' Далее вы пишете тест, что если токен сохранён...'
    #для этого сами поставим true в fake_redis
    auth_statement = 'is_user_confirmed_token:255981'
    await fake_redis.set(auth_statement, 'true')
    
    #опять запускаем обработчик
    await user_text_message(fake_message)
    
    #проверяем, что функция была вызвана с нужным айдишником и сообщением
    mock_delay.assert_called_once_with(255981, 'Угабуга донкиконг')
    
    #смотрим текст ответа, проверяем, что там есть слова,
    #которые обработчик выдает, когда с токеном что-то не так
    #args получит кортеж со всеми строками
    #Прошу прощения, тут нейросеть подсказала, как нормально получить ответ бота
    fake_message.answer.assert_called_once()
    args, _ = fake_message.answer.call_args
    assert 'Сейчас-сейчас *вдох* ' in args[0]
