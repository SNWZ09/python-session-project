# файл, в котором описаны HTTP-исключения
#'вы создаёте BaseHTTPException, который наследуется от HTTPException,
# а затем создаёте набор конкретных исключений для Auth Service.
# Здесь должны быть как минимум UserAlreadyExistsError (409),
# InvalidCredentialsError (401), InvalidTokenError (401),
# TokenExpiredError (401), UserNotFoundError (404),
# PermissionDeniedError (403).'

# импортируем HTTPException, чтобы наш класс
# наследовался от него

from fastapi import HTTPException


# создаем класс, который наследуется от HTTPException
class BaseHTTPException(HTTPException):
    error_num: int = 500
    detailed_description: str = "Ошибка на стороне сервера"

    def __init__(self):
        # с помощью метода супер() передаем номер ошибки и ее текстовое описание
        super().__init__(status_code=self.error_num, detail=self.detailed_description)


class UserAlreadyExistsError(BaseHTTPException):
    error_num = 409
    detailed_description = "409: Пользователь уже существует"
    pass


class InvalidCredentialsError(BaseHTTPException):
    error_num = 401
    detailed_description = "401: Неправильный email или пароль"
    pass


class InvalidTokenError(BaseHTTPException):
    error_num = 401
    detailed_description = "401: Неправильный токен"
    pass


class TokenExpiredError(BaseHTTPException):
    error_num = 401
    detailed_description = "401: Токен устарел"
    pass


class UserNotFoundError(BaseHTTPException):
    error_num = 404
    detailed_description = "404: Пользователь не найден"
    pass


class PermissionDeniedError(BaseHTTPException):
    error_num = 403
    detailed_description = "403: Отказано в доступе"
    pass
