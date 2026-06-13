#создаём базовый класс (DeclarativeBase), 
#от которого наследуются все модели
#(взято из урока на платформе)

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
