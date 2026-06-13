#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#добавляем новый импорт datetime, чтобы реализовать поле created_at
#'Например UserPublic с id, email, role, created_at' (из задания)

#публичная схема пользователя (без пароля и хеша)

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    
    #чтобы FastAPI мог возвращать ORM-объекты напрямую как схему
    model_config = {"from_attributes": True}
