#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#думал оставить логику ошибок, которые вылезали тут в случаях
#если почта уже занята, пользователь не найден или 
#был введен неправильный пароль, но понял, что это уже 
#реализовано в BaseHTTPException

#импорт usecases, созданных схем, ошибок
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id

#HTTP-эндпоинты
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


#создаем роутер с тегом auth
router = APIRouter(prefix='/auth', tags=['auth'])

#эндпоинт регистрации
#клиент получит только публичные данные
@router.post('/register', response_model=UserPublic)
async def register(data: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    
    #передаем данные в логику регистрации
    #удаляем тут try и except, потому что usecase сам выкинет нужную ошибку
    return await auth_usecase.register(data)

  
#эндпоинт логина
#'Для /auth/login используется OAuth2PasswordRequestForm, 
#поэтому вы принимаете form: OAuth2PasswordRequestForm = Depends().'
#из задания
#но прошлый код особо не поменяется
@router.post('/login', response_model=TokenResponse)
async def login(    
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):

    #удаляем тут try и except, потому что usecase сам выкинет нужную ошибку
    #так же меняем строчку return TokenResponse(access_token=token),
    #так как auth_usecase.login теперь сам возвращает готовую схему TokenResponse
    return await auth_usecase.login(form_data.username, form_data.password)

        
#эндпоинт получения профиля
@router.get('/me', response_model=UserPublic)
async def get_me(current_user: UserPublic = Depends(get_current_user_id)):
    
    #удаляем тут try и except, потому что usecase сам выкинет нужную ошибку
    return current_user
