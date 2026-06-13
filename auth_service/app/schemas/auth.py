#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе


#схема авторизации
#импорт pydantic, а именно 
#BaseModel, EmailStr (проверка на эл. адрес),
#и Field (для проверки пароля на длину)
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    #проверка эл. адреса
    email: EmailStr
    
    #задаем макс. и мин. длину пароля
    password: str = Field(min_length = 5, max_length = 40)
    
class TokenResponse(BaseModel):

    access_token: str
    
    #стандартный тип токена (как в задании)
    token_type: str = 'bearer'
