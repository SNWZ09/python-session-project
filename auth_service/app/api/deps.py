#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#меняем импорты ошибок и сами ошибки,
#удаляем импорт ChatUseCase, OpenRouterClient, ChatMessageRepository,
#


#импорт функций, которые создают
#и предоставляют сессию базы данных,
#репозитории и usecase-объекты через Depends
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase

#добавляем импорт ошибки и UserPublic для дальнейшего отображения пользователя
#с помощью get_current_user_id()
from app.core.exceptions import InvalidTokenError
from app.schemas.user import UserPublic

#так же добавляем нашу функцию для декодирования токена,
#которую мы используем, чтобы либо декодировать токен и вернуть его,
#либо, если он просрочился, выкинуть ошибку (ошибка реализована будет здесь
#а не в security.py)
from app.core.security import decode_token


#сначала сделаем кнопку авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

#метод создания и закрытия сессии
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
        
#методы получения репозитория пользователей
#используем просто def, тк нет сетевых запросов

def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

    
#метод получения usecase-объекта 
def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)
    
#метод проверки jwt-токена и извлечение id юзера из sub
#Прошу прощения, подсмотрел, было очень сложно разобраться
#с этой проверкой
#тут меняем -> int на -> UserPublic и добавляем AuthUseCase, чтобы получить пользователя
#естественно, всё придет без пароля, так как в AuthUseCase мы брали не User, а UserPublic
#и структуру тоже меняем:
#удаляем credentials_exception = HTTPException, так как у нас 
#уже есть прописанные ошибки в exceptions.py
#добавляем AuthUseCase, которое зависит от get_auth_usecase()
async def get_current_user_id(token: str = Depends(oauth2_scheme), 
                            auth_usecase: AuthUseCase = Depends(get_auth_usecase)) -> UserPublic:
    
    #пытаемся расшифровать токен
    try:
        payload = decode_token(token)
        
        #если decode_token вернул None, поднимаем ошибку
        if not payload:
            raise InvalidTokenError()
            
        #если payload все нормально вернул - пытаемся вытянуть айдишник юзера    
        user_id_after_decode = payload.get('sub')
        
        #если не получилось вытянуть айдишник - поднимаем ошиюку
        if not user_id_after_decode:
            raise InvalidTokenError()
            
        #ищем в БД юзера, ждем ответа от БД и возвращаем юзера
        #с помощтю метода me из usecases/auth.py
        #пишем int, так как из payload мы получаем строку, а в БД id - integer
        
        current_user = await auth_usecase.me(int(user_id_after_decode))
        
        #возвращаем пользователя
        return current_user
        
    except ValueError:
        raise InvalidTokenError
        
