#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#меняем ошибки, которые будут выбрасываться,
#добавляем импорты ошибок, RegisterRequest и TokenResponse
#поменяем User на UserPublic, так как по заданию важно, чтобы в ответах 
#никогда не было пароля
#из-за этого измененями подвергнуться регистрация, логин и me()

#импорт репозитория пользователей, ошибок,
#паролей, а так же пользователей
from app.repositories.users import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


#измененный импорт ошибок и добавленный импорт 
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError
from app.schemas.auth import RegisterRequest, TokenResponse
#так же импортируем UserPublic, а не User
#так как в User есть пароль, а в UserPublic - нет
from app.schemas.user import UserPublic

class AuthUseCase:
    #сначала передаём репозиторий
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    #метод регистрации нового юзера
    #делаем проверку на уникальность эл. адреса
    #хэшируем пароль, всё сохраняем
    #теперь используем схему регистрации и новую ошибку
    async def register(self, data: RegisterRequest) -> UserPublic:
        #если не сложно, напишите в ревью, пожалуйста
        #можно ли эту проверку было сделать в if?
        #или конструкция не позволяет и обязательно нужно сначала
        #присвоить эту проверку переменной existing_user?
        existing_user = await self._user_repo.get_by_email(data.email)
        if existing_user:
            raise UserAlreadyExistsError()
        
        hashed_pswd = hash_password(data.password)
        
        #немного видоизменим return предварительно засунув новые данные в переменную, 
        #а так же поменяем User на UserPublic
        #из-за этого передавать пароль и почту нужно методом create из класса UserRepository
        new_user = await self._user_repo.create(email=data.email, password_hash=hashed_pswd)
        
        #в return превращаем всю информацию о новом юзере в другую форму:
        #model_validate поможет вывести всю информацию, не касающуюся пароля
        
        return UserPublic.model_validate(new_user)
        
    #метод логина существующего юзера
    #теперь тут возвращается TokenResponse, который был прописан в 
    #schemas/auth.py
    async def login(self, email: str, password: str) -> TokenResponse:
        #ищем по эл. адресу
        user = await self._user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        
        #проверяем пароль
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
            
        #генерируем JWT-токен
        token = create_access_token(user_id = user.id, role = user.role)
           
        #и возвращаем его в формате  нашей схемы из auth.py  
        return TokenResponse(access_token = token)
        
    #метод получения профиля по user_id
    #здесь тоже User меняется на UserPublic
    async def me(self, user_id:int) -> UserPublic:
        user = await self._user_repo.get_by_id(user_id)
        
        #если не нашелся - выкидываем ошибку
        if not user:
            raise UserNotFoundError()
            
        #возвращаем ту же схему, что и в регистрации    
        return UserPublic.model_validate(user)
    
    
        
