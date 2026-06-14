#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#удаляем sqlite_path
#переносим сюда все, что удалили для auth_service (то есть OpenRouter)
#добавляем токен телеграм-бота
#и url для подключения к брокеру задач RabbitMQ
#и url для подключения к хранилищу Redis 


#пишем импорты для автоматического считывания переменных из .env
from pydantic_settings import BaseSettings, SettingsConfigDict

#класс для управления настройками приложения 
class Settings(BaseSettings):
    APP_NAME: str
    ENV: str

    JWT_SECRET: str
    JWT_ALG: str

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_SITE_URL: str
    OPENROUTER_APP_NAME: str
    
    #токен телеграм-бота
    TELEGRAM_BOT_TOKEN: str
    
    #url для подключения к брокеру задач и хранилищу
    #все ссылки подтянутся из .env
    RABBITMQ_URL: str
    REDIS_URL: str
    
    #указываем, что переменные нужно читать из файла .env
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8')
    
settings = Settings()
