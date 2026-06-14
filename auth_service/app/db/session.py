#берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
#но немного редактируем:
#тут заметил ошибку в предыдущей работе. При создании фабрики сессий я указал class_=AsyncSession
#это неправильно, так как мы уже используем async_sessionmaker, который изначально (исходя из названия - точно)
#сделан для асинхронной работы
#поэтому параметр class_=AsyncSession я просто удаляю

#создаём асинхронный engine SQLAlchemy и фабрику сессий
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
#импорт настроек (нам потребуется sqlite_path)
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{settings.SQLITE_PATH}'

#создаем engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False
)

#создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False, #чтобы после сохранения мы могли читать данные
)
