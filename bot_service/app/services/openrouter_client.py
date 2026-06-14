#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#меняем класс
#конкретнее - удаляем его и пишем функцию call_openrouter_client,
#которая принимает prompt (историю сообщений мы теперь собираем в payload)
#меняем заголовоки
#ставим корректный API-ключ для Authorization
#(а то он у меня был изначально прописан. Нужно, чтобы он брался из settings)
#так же, теперь пытаесяс открыть асинхронный клиент
#если не получается - выбрасываем ошибку + добавляем ошибки сети
#'В этом файле вы обязаны обрабатывать ошибки сети и ответы не-200,
#чтобы воркер не падал без понятного сообщения.'
#(из задания)


#запрос клиента на базовый URL OpenRouter
#взял httpx из pyproject.toml
import httpx

#импорт настроек для доступа к данным OpenRouter из .env
from app.core.config import settings



#метод принимает список словарей сообщений
#всё это выглядит, как история диалога в формате:
#роль, контент и тд
#возвращает только ответ ИИ
async def call_openrouter_client(prompt: str) -> str:

#собираем заголовки
    headers = {
        'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}',
        'HTTP-Referer': settings.OPENROUTER_SITE_URL,
        'X-Title': settings.OPENROUTER_APP_NAME
    }
    
    #тело запроса
    #(модель и история сообщений)
    payload = {
        'model': settings.OPENROUTER_MODEL,
        'messages': [{"role": "user", "content": prompt}]
    }
    
    #теперь нужно открыть клиент для связи с 'интернетом'
    #так же, на всякий-всякий случай, укажем ещё время 
    #максимального ответа нейросети - 40 секунд
    #(возможно надо будет увеличить)
    #строчку ниже подсмотрел, прошу прощения
    #не понимал, как открыть клиент
    #на платформе async with использовалась только с engine
    #пытаемся открыть клиент или выбрасываем ошибку
    try:
        async with httpx.AsyncClient() as client: 
            response = await client.post(
            f'{settings.OPENROUTER_BASE_URL}/chat/completions',
            json = payload,
            headers = headers,
            timeout = 40.0
        )
        
        #если статус-код не равен 200 - выбрасываем ошибку
        if response.status_code != 200:
            error_detail = response.text
            raise RuntimeError(f'Ошибка OpenRouter {response.status_code}: {error_detail}')
        
        #превращаем ответ из json в словарь и вытаскиваем сам ответ
        data = response.json()
        
        #берем первый вариант ответа и возвращаем 
        return data['choices'][0]['message']['content']
    
    #ошибка сети
    except httpx.HTTPError as e:
        
        #ловим ошибку сети
        print(f'Ошибка при запросе к OpenRouter: {e}')
        
        #и выбрасываем ошибку, чтобы llm_tasks это увидел и выдал предсмертное сообщение
        raise RuntimeError('Ошибка API нейросети. Видимо он все-таки задохнулся.')
    
    


