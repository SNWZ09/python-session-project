#импорт jwt, чтобы декодировать токен
#импорт JWTError, чтобы выкинуть ValueError
#'Если токен неверный или истёк — вы бросаете 
#ValueError или ваше доменное исключение.' (из задания)
#Прошу прощения, что выбрал более легкий путь и буду
#выбрасывать просто ValueError
from jose import jwt, JWTError

#импортируем настройки, тк в декодирование
#нужно засунуть jwt_secret и jwt_alg из .env
from app.core.config import settings

#пишем decode_and_validate(token: str) -> dict
def decode_and_validate(token: str) -> dict:

    #пытаемся декодировать
    #получилось - возвращаем payload
    #не забываем про проблемное место из прошлого проекта
    #сразу пишем algorithms
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms = [settings.JWT_ALG])
        
        return payload
    
    #не получилось - поднимаем ошибку
    except JWTError:
        raise ValueError('Токен неверный или истёк')
