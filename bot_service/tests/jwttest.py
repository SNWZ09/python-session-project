#'Модульные тесты должны проверять, что токен декодируется
#и валидируется корректно. Вы создаёте тестовый токен
#тем же секретом и алгоритмом, затем вызываете 
#вашу функцию проверки decode_and_validate, и проверяете что 
#sub извлекается корректно. Второй тест должен проверять,
#что мусорная строка вместо токена вызывает ошибку. 
#Это нужно, чтобы доказать, что бот не “верит любому тексту”.'
#импорт pytest, jwt, settings и decode_and_validate

import pytest
from jose import jwt
from app.core.config import settings
from app.core.jwt import decode_and_validate


#тест успешного декодирования
def test_decode_and_validate():

    #создаем тестовый токен с таким же секретом и алгоритмом
    #в качестве id возьму номер зачетки
    test_payload_data = {'sub': '255981', 'role': 'user'}
    test_token = jwt.encode(test_payload_data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    
    #вызываем декод энд валидейт
    decoded_test = decode_and_validate(test_token)
    
    #проверяем, что после декодирования sub остался таким же
    assert decoded_test['sub'] == '255981'

#тест мусорной строки вместо токена
def test_decode_and_validate_incorr():

    #пытаемся декодировать
    try:
        decode_and_validate('fakefakefake')
        
        assert False, 'Функция не отработала, как надо.'
    
    #если вылезла ошибка - тест пройден
    except ValueError:
        assert True
