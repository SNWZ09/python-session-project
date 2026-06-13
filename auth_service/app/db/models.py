#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#удаляем класс ChatMessage, так как в будущем он будет перенесён 
#(или полностью видоизменён, пока не могу нормально сказать)
#в bot_service (так же, как и openrouter)
#удаляем ForeignKey и relationship из импорта, так как
#они нужны были здесь только для ChatMessage
#ещё немного поменял коммент, который объяснял, почему я решил поставить дефолтную роль user
#и добавил коммент, который объясняет created_at


#здесь опишем ORM-модели.
#Пользователь с полями: id, email, password_hash,
#role, created_at.

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    
    #опишем столбцы таблицы
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    #'в роли решил написать дефолтное значение, т.к., мне кажется,
    #что это важно предусмотреть' - странное и недостаточное объяснение
    #дефолтную роль нужно поставить, чтобы БД сама автоматически присваивала её пользователям
    #если этого не сделать - придется писать роль каждому новому пользователю
    # + не уверен, что это работает именно так (возможно, есть ещё какие-то методы защиты),
    #но есть риск того, что отсутствие этого параметра позволит написать пользователю
    #при регистрации в графе role значение admin
    #и тогда новый пользователь сразу будет с админскими правами - ситуация так себе
    role: Mapped[str] = mapped_column(String, default='user')
    
    #добавлем столбец с временем создания
    #в параметрах учитываем таймзону пользователя, чтобы не было путаницы с временем создания
    #server_default=func.now() - делает так, что в момент получения команды БД смотри на часы
    #и подставляет текущее время
    #nullable=False - запрещает создавать пользователя без даты регистрации
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

