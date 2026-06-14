#импортируем asyncio
import asyncio

#импортируем aiogram - каркас приложения, который берёт на себя типовую инфраструктуру вокруг Bot API
#(из материалов на платформе)
from aiogram import Bot

#импортируем celery и настройки, так как нам понадобится
#токен телеграм-бота
from app.infra.celery_app import celery_app
from app.core.config import settings

#импортируем функцию обращения к нейросети
from app.services.openrouter_client import call_openrouter_client

#создаем бота, чтобы воркер мог отправлять сообщения в телеграм
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

#создаем декоратор, чтобы превратить функцию llm_request в фоновую задачу
#это нужно, чтобы в случае запроса к боту одним юзером, он не помирал
#для всех остальных юзеров, а продолжал принимать запросы и 
#отправлять их в Редис
@celery_app.task(name='app.tasks.llm_tasks.llm_request')
def llm_request(tg_chat_id: int, prompt: str):   
    
    #проблема в том, что мы не можем напрямую вызывать асинхронную функцию,
    #тк Celery синхронная библиотека
    #для того, чтобы решить проблему синхронности (Celery) и асинхронности
    #(aiogram и запросы к нейросети), ниже напишем функцию process_llm_request,
    #которую запустим с помощтю asyncio.run()
    asyncio.run(process_llm_request(tg_chat_id, prompt))

#пишем запрос к нейросети и её ответ юзеру    
async def process_llm_request(tg_chat_id: int, prompt: str):

    #захотел добавить немного себя нейросети
    #хочу, чтоб все ответы он писал так, как будто он дико запыхался 
    #и ему не хватает воздуха
    context = 'Весь ответ пиши так, как будто ты дико запыхался. Добавляй *Дышет*, *Вздыхает* и прочее в свои ответы'
    
    #пытаемся сделать запрос к нейросети
    try:
        response_text_with_context = await call_openrouter_client(prompt + context)
        
        #отправляем ответ юзеру
        await bot.send_message(chat_id=tg_chat_id, text=response_text_with_context)
     
    #если что-то где-то упало - выкидываем ошибку
    except Exception:
        await bot.send_message(
            chat_id=tg_chat_id, 
            text='*Фух* ааааа, как я запыхался... *Дышит* *Пытается отдышаться*. Что-то *выдыхнул ртом* поломалось... *Тяжко дышит*. *Умирает*.')
    
    #закрываем сессию бота после ответа или ошибки
    finally:
        await bot.session.close()
    
    
