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
    app_name: str
    env: str

    jwt_secret: str
    jwt_alg: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str
    
    #токен телеграм-бота
    bot_token: str
    
    #url для подключения к брокеру задач и хранилищу
    #все ссылки подтянутся из .env
    rabbitmq_url: str
    redis_url: str
    
    #указываем, что переменные нужно читать из файла .env
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8')
    
settings = Settings()
