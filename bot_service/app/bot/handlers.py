#'Handler - это обычная функция (чаще async), которая вызывается aiogram-ом, когда пришло событие и оно подошло под условия.'
#из материалов платформы

#импортируем роутер, чтобы навесить на него обработчики с помощью Command
from aiogram import Router
from aiogram.filters import Command

#так же импортируем Message, чтобы можно было работать с конкретными ответами бота
#и с сообщениями в принципе
from aiogram.types import Message

#импортируем проверку токена, подключение к Редис и фоновую задачу Celery
#'Здесь же должен быть обработчик обычного текста: 
#он проверяет наличие токена в Redis, валидирует токен,
#после чего отправляет задачу в Celery (llm_request.delay(...))'
#(из задания)
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request


#создаем роутер
#его надо будет подключить в dispatcher.py
router = Router()

#команда старт, которая потребует от юзера прислать JWT-токен,
#чтобы авторизироваться
#'обработчик будет вызван только тогда, 
#когда входящее сообщение является командой /start.'
#(из материалов на платформе), только я немного переделал
#можно было бы просто написать CommandStart(), но мне захотелось по-другому
#надеюсь, не ошибка
@router.message(Command('start'))
async def bot_start(message: Message):
    
    #ждем старта и отправляем сообщение
    await message.answer('Прив... *Дышит* Приве *ха....ха* т. Давай *глубойкий вздох* свой JWT-токен, чтобы я тебя впустил *ФУУУУУУУУУУУУУУУУУУУУУУУУУУУУУХ* *Дикая отдышка*.')
    

#теперь обработка токена
@router.message(Command('token'))
async def token_check(message: Message):
    
    #разделяем сообщение по пробелу
    user_command_split = message.text.split()
    
    #проверяем, что юзер не забыл поставить пробел
    if len(user_command_split) < 2:
        await message.answer('Токен... *Вдох* Где??.. ха-...-ху. Пиши /token <токен>..')
        return
        
    #берем токен юзера  
    user_token = user_command_split[1]
    tg_chat_id = message.chat.id
    
    try:
        #проверяем токен
        decode_and_validate(user_token)
        
        #если все норм - сохраняем в Редис
        redis_client = await get_redis()
        auth_statement = f'is_user_confirmed_token:{tg_chat_id}'
        
        #если ошибка не вылезла - был прислан правильный токен
        #записываем в Редис, что пользователь отныне авторизован
        #чуть не забыл, что токен имеет срок годности
        #в .env для auth_service указано 60 минут
        #как записать истечение срока токена посмотрел в интернете
        #Прошу прощения
        await redis_client.set(auth_statement, 'true', ex=3600)
        
        #если все нормально - выводим сообщение
        await message.answer('С токе ху-.......-ху *хрипло* все нормально с токеном *глубочайший вдох, который знаменует отчаяние от надвигающегося вопроса*. Какой у тебя вопрос?')
        
    #decode_and_validate говорит, что с токеном что-то не так - поднимаем ошибку    
    except Exception as e:
        await message.answer('С токеном что-то не та.... ха-....ха-...ху. неправильный токен или *Вдох* *Мало забрал воздуха, поэтому ещё вдох* или у него срок истек. Давай другой')
        

#теперь обработка всех остальных сообщений
@router.message()
async def user_text_message(message: Message):
    
    #запоминаем id чата в телеграмме, чтобы Celery знал, куда отправлять ответ
    tg_chat_id = message.chat.id
    
    #и сам текст пользователя
    user_text = message.text
    
    #подключаемся к Редису, чтобы сохранить токен
    #'обработчик команды /token <jwt>, который сохраняет токен в Redis
    #под ключом, связанным с Telegram user_id'
    #(из задания)
    redis_client = await get_redis()
    
    #создаем ключ аутентификации, чтобы, при обращении к нему, 
    #Редис смотрел, прошел ли юзер аутентификацию
    #(то есть прислали нормальный токен)
    #если да - пускаем к нейросети
    auth_statement = f'is_user_confirmed_token:{tg_chat_id}'
    
    #теперь проверка на то, авторизован ли пользователь
    is_user_authorized = await redis_client.get(auth_statement)
    
    #если пользователь авторизован - то есть if выдало true
    #отправляем задачу в очередь RabbitMQ с помощью delay() 
    #(из урока 4. Оптимизация и интеграция сервисов. Celery и Celery Beat),
    #чтобы не блокировать бота
    if is_user_authorized:
        llm_request.delay(tg_chat_id, user_text)
        
        #отправляем сообщение, что всё дошло и скоро будет ответ
        await message.answer('Сейчас-сейчас *вдох* *выдох* *вдох* скоро дам ответ... *Глубокий выдох* хаааааааа. Дай отдышаться *Вдох*')
    
    else:
        await message.answer('Токен... *Вдох* Где??.. ха-...-ху. Пиши /token <токен>..')
