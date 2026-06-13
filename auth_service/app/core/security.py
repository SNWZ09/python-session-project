#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#добавляем логику времени жизни токена в decode_token
#+ немного меняем пояснения и сделаем импорт JWTError


#импорты для работы с временем
#используем их, чтобы задать срок годности для токена
#timezone используем, чтобы 'унифицировать' время его создания
#timedelta используем для вычисления разницы во времени
from datetime import datetime, timedelta, timezone

#импорт для хэширования пароля
from passlib.context import CryptContext

#импорт для работы с jwt-токенами и их ошибками
from jose import jwt, JWTError

#импорт для подключения созданных ранее настроек
from app.core.config import settings

#используем алгоритм bcrypt
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    #функция берет обычный пароль и превращает его
    #в 'непонятную' строку
    return pwd_context.hash(password)
    
def verify_password(password: str, hashed_password: str) -> bool:
    #функция проверяет, что введённый пароль 
    #соответствует сохранённому хэшу
    return pwd_context.verify(password, hashed_password)
    
def create_access_token(user_id: int, role: str) -> str:
    #вычисляем, когда токен истечёт
    #для этого берем текущее время и прибавляем к нему
    #количество минут, указанных в настройках
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    #запоминаем время выдачи токена
    iat = datetime.now(timezone.utc)
    
    #создаем payload, чтобы связать его с токеном
    payload = {
        'sub': str(user_id), #владелец токена
        'role': role, #роли владельца токена
        'exp': expire, #время, когда токен перестанет работать
        'iat': iat #время, когда токен был создан
    }

    #с помощью jwt.encode подписываем наш payload
    #секретным ключом с помощью алгоритма 
    #(всё берётся из config.py)
    #и получаем итоговый токен
    return jwt.encode(payload, settings.jwt_secret, algorithm = settings.jwt_alg)
    
#теперь осталось создать функцию декодирования токена
#используем те же данные, что и в jwt.encode
#'в settings.jwt_alg используем квадратные скобки
#потому что без них у меня не сработало...
#не знаю почему, честно.. Прошу прощения'
#в прошлой работе я не смог ответить, почему нужны квадратные скобки
#как я понял, они нужны, потому что параметр algorithms принимает список из всех
#разрешенных алгоритмов и проверяет, есть ли присланный алгоритм в списке разрешенных
#надеюсь, что стало объяснение стало немного четче
#тем не менее, дело в том, что раньше у меня было написано 
#algorithm, а не algorithms - и из-за этого мне кажется,
#что код работал бы даже при учете, что я не поставил бы квадр. скобки
#теперь про логику времени жизни токена
#в задании сказано 'вы должны корректно валидировать подпись и время жизни токена.'
#из-за этого структура функции поменяется:
#мы будем пытаться декодировать токен, но если время его жизни вышло - возвращать ничего не будем
def decode_token(token: str) -> dict | None:
    try:
        #пытаемся декодировать
        encoded_payload = jwt.decode(token, settings.jwt_secret, algorithms = [settings.jwt_alg])
        return encoded_payload
    
    except JWTError:
        #если время жизни вышло - будет JWTError
        #если эта ошибка вылезла - ничего не возвращаем
        return None
