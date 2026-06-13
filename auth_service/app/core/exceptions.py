#файл, в котором описаны HTTP-исключения
#'вы создаёте BaseHTTPException, который наследуется от HTTPException,
#а затем создаёте набор конкретных исключений для Auth Service. 
#Здесь должны быть как минимум UserAlreadyExistsError (409), 
#InvalidCredentialsError (401), InvalidTokenError (401), 
#TokenExpiredError (401), UserNotFoundError (404), 
#PermissionDeniedError (403).'

#импортируем HTTPException, чтобы наш класс
#наследовался от него

from fastapi import HTTPException

#создаем класс, который наследуется от HTTPException
class BaseHTTPException(HTTPException):
    'Ошибка на стороне сервера'
    pass
    
    
class UserAlreadyExistsError(BaseHTTPException):
    '409: Пользователь уже существует'
    pass
    
class InvalidCredentialsError(BaseHTTPException):
    '401: Неправильный email или пароль'
    pass
    
class InvalidTokenError(BaseHTTPException):
    '401: Неправильный токен'
    pass
    
class TokenExpiredError(BaseHTTPException):
    '401: Токен устарел'
    pass
    
class UserNotFoundError(BaseHTTPException):
    '404: Пользователь не найден'
    pass
    
class PermissionDeniedError(BaseHTTPException):
    '403: Отказано в доступе'
    pass
    

