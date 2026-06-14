# импорт пайтеста, настроки которого указаны в pytest.ini
import pytest

#'запрос выполняется через AsyncClient,
# а затем состояние системы проверяется через await в репозитории/сессии.
# Именно поэтому тест должен быть async def.'
# (из урока 6. Production-практики FastAPI. Ошибки и тестирование. Асинхронное тестирование FastAPI)
from httpx import AsyncClient, ASGITransport

# создаём асинхронный engine SQLAlchemy и фабрику сессий
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# импортируем приложение, базовую модель и выдачу сессий
from app.main import app
from app.db.base import Base
from app.api.deps import get_session

#'Интеграционные тесты должны проверять реальный пользовательский сценарий через HTTP.
# Для этого вы поднимаете FastAPI приложение в тесте, подменяете зависимость get_db так,
# чтобы использовать in-memory SQLite'
# из задания
# подключаемся к бд в оперативной памяти
test_db_url = 'sqlite+aiosqlite:///:memory:'

# создаем engine для тестов
engine_for_test = create_async_engine(test_db_url, echo=False)

# создаем фабрику сессий для тестов
# чтобы после сохранения мы могли читать данные expire_on_commit=False
TestSessionLocal = async_sessionmaker(engine_for_test, expire_on_commit=False)


# делаем асинхронную фикстуру для создания и удаления таблиц
# долго думал над тем, как это нормально сделать
# в итоге нашел в документации pytest (https://docs.pytest.org/en/stable/how-to/fixtures.html)
# главу Autouse fixtures (fixtures you don’t have to request)
# решил добавить этот autouse, чтобы асинхронная функция ниже сама запускалась
# перед каждым тестом
# как я понял, если этого не сделать, то тесты будут либо падать, либо не запускаться
# так как в оперативной памяти не будет таблиц
@pytest.fixture(autouse=True)
async def test_create_db():
    async with engine_for_test.begin() as conn:
        # cоздаем бд
        await conn.run_sync(Base.metadata.create_all)

    # pytest делает тесты
    yield

    # после теста удаляем бд, чтобы новый тест начался с чистой бд
    async with engine_for_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# выдаем тестовую сессию
async def get_test_session():
    async with TestSessionLocal() as session:
        yield session


#'Для этого вы поднимаете FastAPI приложение в тесте, подменяете зависимость get_db так,
# чтобы использовать in-memory SQLite, и выполняете запросы через httpx ASGITransport.'
# (из задания)
#'Если приложение использует зависимости FastAPI,
# то предпочтительнее подменять зависимости через dependency_overrides,
# а не патчить импорты.'
# (из урока 1. Введение. Production-практики FastAPI. Ошибки и тестирование)
app.dependency_overrides[get_session] = get_test_session


# фикстура клиента
# делаем имитацию запросов через httpx ASGITransport
@pytest.fixture
async def test_client():
    transport = ASGITransport(app=app)

    # передаем транспорт вместо app
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
