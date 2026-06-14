#'в учебной постановке удобнее: 
#FastAPI и бот — как разные процессы в docker-compose.'
#из задания
import asyncio
from fastapi import FastAPI
from aiogram import Bot

#импорт настроек и Dispatcher с подключенным роутерем из handlers.py
from app.core.config import settings
from app.bot.dispatcher import dp

#собираем приложение
app = FastAPI(title=settings.APP_NAME)

#теперь бота по токену из настроек
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

#прописываем те же события, что и в main.py для auth_service
#для стартапа пишем start_polling() 
#(из урока 7. Оптимизация и интеграция сервисов. Разработка Telegram-бота)
#чтобы бот постоянно смотрел, нет ли новых сообщений
#'C этого момента бот начинает постоянно 
#получать обновления от Telegram и обрабатывать сообщения.'
@app.on_event('startup')
async def startup_event():
    asyncio.create_task(dp.start_polling(bot))
    
#теперь событие выключения
#просто закрываем сессию бота
@app.on_event('shutdown')
async def shutdown_event():
    await bot.session.close()
    
#и добавляем эндпоинт health
@app.get('/health', tags=['bot-health'])
async def health_check():
    return {'status': 'ok', 'service': 'bot-service', 'environment': settings.ENV}
