# Двухсервисная система LLM-консультаций

В рамках проекта разрабатывается распределённая система, состоящая из двух логически и технически независимых сервисов, каждый из которых выполняет строго определённую роль.

### Архитектура
1. Auth Service (FastAPI) - Auth Service предоставляет веб-API и Swagger. В этом сервисе реализуются регистрация пользователя, вход (логин) и выдача JWT. Сервис хранит пользователей в базе, хранит пароль только в виде хеша и формирует JWT с полями sub (id пользователя), role и временем жизни. Этот сервис является единственным местом, где выполняется “выпуск” токенов и управление пользователями.
   - Предоставляет регистрацию
   - Предоставляет логин
   - Предоставляет JWT-токен
   - Предоставляет возможность посмотреть профиль пользователя
   - Хранит в базе пользователей и хеш-пароли
2. Bot Service (aiogram) - содержит Telegram-бота на aiogram. Основная логика: бот принимает сообщения пользователя, проверяет наличие JWT и валидирует его. Если токен валиден, бот отправляет запрос к LLM и возвращает ответ. Если токен отсутствует или неверный, бот отказывает в доступе и просит пользователя авторизоваться через Auth Service.
   - Проверяет наличие токена
   - Валидирует токен
   - Привязывает токен к конкретному пользователю в Telegram
   - Принимает сообщения пользователя
3. Redis - используется, как хранилище, в котором указывается, авторизован ли пользователь, который обращается к боту;
4. RabbitMQ - является брокером. Реализует асинхронную передачу запросов между ботом и воркером.
5. Celery - фоновый процесс, который забирает задачи из очереди и обращается к OpenRouter, после чего отправляет свой ответ пользователю. 

### Сценарий работы
Сценарий работы выглядит следующим образом:
1. Новый пользователь регистрируется через Auth Service (Swagger);
2. После регистрации пользователь входит в Auth Service и получает свой JWT-токен (Swagger);
3. Пользователь сохраняет полученный токен (Swagger);
4. Когда пользователь собирается взаимодействовать с чат-ботом, он пишет /start (Bot Service), после чего последний попросит его ввести токен, полученный при авторизации;
5. Пользователь присылает ему токен в формате /token <токен_пользователя> (Bot Service);
6. Чат-бот принимает токен, выполняет его декодирование и валидацию (Bot Service);
7. Если токен является корректным, бот сохраняет статус авторизации пользователя и связывает его с Telegram (Bot Service - Redis);
8. После этого бот пишет, что токен подошел (Bot Service);
9. Пользователь отправляет своё сообщение боту (Bot Service);
10. Бот проверяет, что в Redis есть действующая авторизация (Bot Service - Redis);
11. Если существует действующая авторизация, бот публикует задачу (Bot Service - RabbitMQ);
12. Celery-воркер получает задачу из RabbitMQ, взаимодействует с нейросетью, формирует итоговый ответ и отправляет его пользователю в Telegram (RabbitMQ - Celery-воркер - OpenRouter API).

# Скриншоты
## Регистрация пользователя
![Регистрация пользователя](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/Swagger%201%20-%20%D0%A3%D1%81%D0%BF%D0%B5%D1%88%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F.png?raw=true)

## Логин и выдача токена
![Логин и выдача токена](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/Swagger%202%20-%20%D0%9B%D0%BE%D0%B3%D0%B8%D0%BD%20%D0%B8%20%D0%B2%D1%8B%D0%B4%D0%B0%D1%87%D0%B0%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0.png?raw=true)

## Авторизация
![Авторизация](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/Swagger%203%20-%20%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F.png?raw=true)

## /auth/me
![/auth/me](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/Swagger%204%20-%20%D0%AD%D0%BD%D0%B4%D0%BF%D0%BE%D0%B8%D0%BD%D1%82%20me.png?raw=true)

## Telegram 1 - Запуск бота
![Telegram 1 - Запуск бота](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/Telegram%201%20-%20%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%B1%D0%BE%D1%82%D0%B0.png?raw=true)

## Telegram 2 - Подтверждение токена и ответ бота
![Telegram 2 - Подтверждение токена и ответ бота](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/Telegram%202%20-%20%D0%9F%D0%BE%D0%B4%D1%82%D0%B2%D0%B5%D1%80%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%20%D0%B8%20%D0%BE%D1%82%D0%B2%D0%B5%D1%82%20%D0%B1%D0%BE%D1%82%D0%B0.png?raw=true)

## RabbitMQ 1 - Логин
![RabbitMQ 1 - Логин](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/RabbitMQ%201%20-%20%D0%9B%D0%BE%D0%B3%D0%B8%D0%BD.png?raw=true)

## RabbitMQ 2 - Главная страница
![RabbitMQ 2 - Главная страница](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/RabbitMQ%202%20-%20%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0.png?raw=true)

## RabbitMQ 3 - График очереди
![RabbitMQ 3 - График очереди](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/RabbitMQ%203%20-%20%D0%93%D1%80%D0%B0%D1%84%D0%B8%D0%BA%20%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D0%B8.png?raw=true)

## Тест для auth_service
![Тест для auth_service](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/%D0%A2%D0%B5%D1%81%D1%82%20%D0%B4%D0%BB%D1%8F%20auth_service.png?raw=true)

## Тест для bot_service
![Тест для bot_service](https://github.com/SNWZ09/python-session-project/blob/main/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D1%8B/%D0%A2%D0%B5%D1%81%D1%82%20%D0%B4%D0%BB%D1%8F%20bot_service.png?raw=true)


#### P.S.
Для тестов вписал в .env TELEGRAM_BOT_TOKEN = 111133324:StepaStepaStepaTokennum1111333242
Для итоговой работы использовал модель openrouter/free
